

def show_titles_ratings(titles, ratings):
    """show titles and ratings in a bar chart"""
    import matplotlib.pyplot as plt
    import numpy as np

    # create a bar chart
    plt.bar(titles, ratings)

    # add a title
    plt.title('Titles and Ratings')

    # add labels
    plt.xlabel('Titles')
    plt.ylabel('Ratings')

    # show the plot
    plt.show()

show_titles_ratings(['A', 'B', 'C'], [1, 2, 3])
