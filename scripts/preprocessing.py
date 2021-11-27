"""The preprocessing script."""
import re
import dateparser
import pandas as pd
from bs4 import BeautifulSoup

# Set some regex filters
FILTER_ID = '^[0-9\\.]+'
FILTER_DOCTYPE = '(?<=[0-9\\_]\\_)[a-z A-Z]+(?=\\_)'
FILTER_DATE = '[0-9-?]+(?=.pftm_df$)'
FILTER_SENDER = '\nvan|\nVan:|\n\n   Van|\n\nFrom'
FILTER_BETTER_DATE = '(?<=Date : )[0-9-]{3,5}-20[0-9]{2} [0-9:]{8}'
FILTER_VERZONDEN = 'Verzonden: (.*)'
FILTER_DATUM = 'Datum: (.*)'
FILTER_AAN = '\n\nAan:(.*)'
FILTER_TO = '\nTo(.*)'


def remove_noise(ftm_df):
    """
    Remove noise of the original FTM dataset.

    Parameters
    ----------
    ftm_df : pandas.DataFrame
        original FTM dataset.

    Returns
    -------
    pandas.DataFrame
        pandas.DataFrame with two columns, title and abstract with removed
        noise.

    """
    ftm_df = ftm_df.dropna()
    ftm_df = ftm_df.rename(columns={"file_name_sort": "title", "content": "abstract"})
    remove = ['.DS_Store', 'NaN', 'Readme.md']

    return ftm_df[~ftm_df.title.isin(remove)]


def prettify(text, newline=False, carriage=False, translate_table=None):
    """
    Prettify a string.

    Parameters
    ----------
    text : str
        text to be prettified.
    newline : bool, optional
        replace newline. The default is False.
    carriage : bool, optional
        replace carriage return. The default is False.
    translate_table : bool, optional
        use a translator. The default is None.

    Returns
    -------
    string
        prettified string.

    """
    text = BeautifulSoup(text, 'html.parser').get_text()
    if carriage:
        text = text.replace('\r', '')
    if newline:
        text = text.replace('\n', '')
    if translate_table:
        text = text.translate(translate_table)
    return str(text)


def prettify_abstract(ftm_df):
    """
    Prettify the abstract.

    Parameters
    ----------
    ftm_df : pandas.DataFrame
        denoised FTM dataset.

    Returns
    -------
    ftm_df : pandas.DataFrame
        FTM dataset with HTML parsed abstract.

    """
    # translate_table = dict((ord(char), None) for char in string.punctuation)
    ftm_df.abstract = ftm_df.abstract.apply(
        prettify, newline=False, carriage=True, translate_table=None)
    return ftm_df


def search_id_type_date(ftm_df):
    """
    Find ID, type, and date of objects in the title.

    Parameters
    ----------
    ftm_df : pandas.DataFrame
        FTM dataset.

    Returns
    -------
    ftm_df : pandas.DataFrame
        FTM dataset with id, type, and date.

    """
    ftm_df['doc_id'] = ftm_df.title.apply(
        lambda title: re.search(
            FILTER_ID,
            title).group(0) if re.search(
            FILTER_ID,
            title) else None)
    ftm_df['doc_type'] = ftm_df.title.apply(
        lambda title: re.search(
            FILTER_DOCTYPE,
            title).group(0) if re.search(
            FILTER_DOCTYPE,
            title) else "Onbekend")
    ftm_df['date'] = ftm_df.title.apply(
        lambda title: dateparser.parse(
            re.search(
                FILTER_DATE,
                title).group(0)) if re.search(
            FILTER_DATE,
            title) else None)
    return ftm_df


def split_abstracts(ftm_df):
    """
    Split the mail abstract (item content) into different mails.

    This is required to find the 'novel' email, and the rest of the threat. We
    create a new row for each email in the threat, but it keeps the ID of the
    'novel email'. We add two boolean flags for is_novel, and
    is_threat_starter.

    Parameters
    ----------
    ftm_df : pandas.DataFrame
        FTM dataset with prettified abstracts.

    Returns
    -------
    pandas.DataFrame
        FTM dataset with a new row for each email, and flags for is_novel and
        is_threat_starter.

    """
    # Create a list of strings from novel email and its forwards or reactions
    ftm_df['new_abstract'] = ftm_df[ftm_df.title.str.contains('RE  ') | ftm_df.title.str.contains(
        'FW  ')].abstract.apply(lambda row: re.split(FILTER_SENDER, row))

    # Create a list of is_novel. First email is novel (1), the rest is
    # forwards or reactions (0). Similar for is_threat_starter
    ftm_df['is_novel'] = ftm_df[ftm_df.title.str.contains('RE  ') | ftm_df.title.str.contains(
        'FW  ')].new_abstract.apply(lambda row: [1] + [0] * (len(row) - 1))
    ftm_df['is_threat_starter'] = ftm_df[ftm_df.title.str.contains('RE  ') |
                                         ftm_df.title.str.contains('FW  ')
                                         ].new_abstract.apply(
                                             lambda row: [0] * (len(row) - 1) + [1])
    # explode the lists
    ftm_df = ftm_df.explode(['is_novel', 'new_abstract', 'is_threat_starter'])
    ftm_df = ftm_df.reset_index()
    ftm_df.abstract = ftm_df.new_abstract.fillna(ftm_df.abstract)
    return ftm_df.drop(columns=['new_abstract'])


def improve_dating(ftm_df):
    """
    Find a better date from object content.

    Parameters
    ----------
    ftm_df : pandas.DataFrame
        FTM dataset with date from title.

    Returns
    -------
    ftm_df : pandas.DataFrame
        FTM dataset with betterDate from abstract.

    """
    ftm_df["betterDate"] = ftm_df.abstract.apply(
        lambda row: dateparser.parse(
            re.search(
                FILTER_BETTER_DATE,
                row).group(0)) if re.search(
            FILTER_BETTER_DATE,
            row) else None)
    return ftm_df


def get_date_from_abstract(ftm_df):
    """
    Get the date from the abstracts.

    Parameters
    ----------
    ftm_df : pandas.DataFrame
        FTM dataset with date from title.

    Returns
    -------
    pandas.DataFrame
        FTM dataset with betterDate from abstract.

    """
    ftm_df['tmp'] = ftm_df[ftm_df.is_novel == 0].abstract.apply(lambda row: re.search(
        FILTER_VERZONDEN, row).group(1) if re.search(FILTER_VERZONDEN, row) else None)
    ftm_df['tmp2'] = ftm_df[ftm_df.is_novel == 0].abstract.apply(lambda row: re.search(
        FILTER_DATUM, row).group(1) if re.search(FILTER_DATUM, row) else None)

    # Combine both temporary dates and strip trailing spaces
    ftm_df['tmp'] = ftm_df['tmp'].fillna(ftm_df['tmp2']).str.strip()
    ftm_df.tmp = ftm_df[ftm_df.is_novel == 0].tmp.apply(
        lambda row: dateparser.parse(row) if row else None)
    ftm_df.tmp = pd.to_datetime(ftm_df.tmp, utc=True)
    ftm_df = improve_dating(ftm_df)
    ftm_df.betterDate = ftm_df.tmp.fillna(ftm_df.betterDate)
    return ftm_df.drop(columns=['tmp', 'tmp2'])


def get_sender(ftm_df):
    """
    Get sender of emails.

    Parameters
    ----------
    ftm_df : pandas.DataFrame
        FTM dataset with unknown email senders.

    Returns
    -------
    ftm_df : pandas.DataFrame
        FTM dataset with known email senders for RE and FW emails.

    """
    ftm_df['email_sender'] = ftm_df[ftm_df.title.str.contains('RE  ') |
                            ftm_df.title.str.contains('FW  ')
                            ].abstract.apply(lambda row: None
                                             if row.split('\n', 1)[0] == ''
                                             else row.split('\n', 1)[0])
    return ftm_df


def get_retriever(ftm_df):
    """
    Get retrievers of emails.

    Parameters
    ----------
    ftm_df : pandas.DataFrame
        FTM dataset with unknown email retrievers.

    Returns
    -------
    pandas.DataFrame
        FTM dataset with known email retreivers for type Mail.

    """
    ftm_df['receiver_aan'] = ftm_df[ftm_df.doc_type == 'Mail'].abstract.apply(lambda row: re.search(
        FILTER_AAN, row).group(1) if re.search(FILTER_AAN, row) else None)
    ftm_df['receiver_to'] = ftm_df[ftm_df.doc_type == 'Mail'].abstract.apply(lambda row: re.search(
        FILTER_TO, row).group(1) if re.search(FILTER_TO, row) else None)
    ftm_df['email_receiver'] = ftm_df['receiver_aan'].fillna(ftm_df['receiver_to'])
    return ftm_df.drop(columns=['receiver_aan', 'receiver_to'])


def clean_title(title):
    """
    Clean title.

    Parameters
    ----------
    title : str
        title of FTM dataset.

    Returns
    -------
    title : str
        cleaned title of FTM dataset.

    """
    title = re.sub('^[0-9\\.]+_+[a-z A-Z]+_', '', title)
    title = re.sub('[0-9\\-]+.pftm_df$', '', title)
    title = re.sub('.msg_', ' ', title)
    return title
