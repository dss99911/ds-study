

from nltk.tokenize import RegexpTokenizer

whitespace_tokenizer = RegexpTokenizer(r'\s+', gaps=True)
ascii_tokenizer = RegexpTokenizer(r'[a-zA-Z0-9_]+', gaps=False)

a = whitespace_tokenizer.tokenize("text abc def")
b = ascii_tokenizer.tokenize("text!1bce,erf")
#%%