"""Main script to preprocess FTM data."""
import load_data
import preprocessing as pp

# load data from the FTM repo. Comment if already downloaded and saved.
load_data.get_and_save_ftm_data('https://github.com/ftmnl/asr/raw/main/data/allExport.csv', 
                                '../data/allExport.csv')

# load the locally saved dataset
df = load_data.get_data('../data/allExport.csv')

# remove some noise form the original dataset
df = pp.remove_noise(df)

# parse html abstract
df = pp.prettify_abstract(df)

# parse id type and date from the title
df = pp.search_id_type_date(df)

# split each email into a new row, add is_novel and is_threat_starter flag
df = pp.split_abstracts(df)

# get the date from abstract
df = pp.get_date_from_abstract(df)

# get the sender of the email
df = pp.get_sender(df)

# get the retriever of the email
df = pp.get_retriever(df)

# clean the title
df.title = df.title.apply(pp.clean_title)

# save the processed data
df.to_csv('../data/processed_data.csv', index=False, sep='|')
