from matplotlib import pyplot as plt
from collections import Counter
from wordcloud import WordCloud

def show_counter_bar(counter: Counter, size: int, title: str=None):
    y = list(range(size))
    key, counts = zip(*counter.most_common(size))

    plt.figure(figsize=(10, 8))
    plt.barh(y, counts)
    plt.title(title)
    plt.yticks(y, key)
    plt.show()


def show_word_cloud(counter: Counter, title: str=None):
    plt.figure(figsize=(10, 8))
    wc = WordCloud(colormap='Greys', background_color='white')
    im = wc.generate_from_frequencies(counter)
    plt.imshow(im, interpolation='bilinear')
    plt.axis("off")
    plt.title(title)

    plt.show()