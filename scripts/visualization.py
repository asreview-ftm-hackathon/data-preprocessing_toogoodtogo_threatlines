import matplotlib.pyplot as plt
import wordcloud
import pandas as pd
from nltk.corpus import stopwords
import nltk

# load dutch stopwords
nltk.download('stopwords')
dutch_stopwords = stopwords.words('dutch')

DPI = 50


def black_color_func(word, font_size, position, orientation,
                     random_state=None, **kwargs):
    """Make word cloud black and white."""
    return("hsl(0,100%, 1%)")


def word_cloud(words,
               caption=None,
               output_fp=None,
               random_state=None,
               width=400,
               height=200,
               max_words=100,
               **wordcloud_kwargs):
    """Word cloud for texts."""
    # create word cloud text
    text = " ".join(str(word) for word in words)

    # generate word cloud images
    wc = wordcloud.WordCloud(stopwords=wordcloud.STOPWORDS.update(dutch_stopwords),
                             max_words=max_words,
                             random_state=random_state,
                             background_color="white",
                             width=width,
                             height=height,
                             font_path='arial.ttf',
                             **wordcloud_kwargs).generate(text)

    wc.recolor(color_func=black_color_func)
    # render plot
    plt.figure(figsize=(15, 10))
    plt.imshow(wc, interpolation="bilinear")
    if caption:
        plt.set_title(caption)
    plt.axis("off")

    # save or show
    if output_fp:
        plt.tight_layout(pad=1)
        plt.savefig(output_fp, dpi=100)
    else:
        plt.show()


if __name__ == "__main__":
    df = pd.read_csv(r'../data/processed_data.csv', sep='|')
    mail = df.abstract
    word_cloud(mail, width=3000, height=2000, max_words=250,
               output_fp='../figures/wordcloud.png')
