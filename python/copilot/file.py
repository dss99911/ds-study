


def save_text(file_name, text):
    """
    Save text to file.
    """
    with open(file_name, 'w') as f:
        f.write(text)