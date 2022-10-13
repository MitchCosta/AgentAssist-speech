import re


def clean_tokenize(text: str, stop_words: list):

    # pre-process the new received text, similar to answer_title in cisco_data
    # clean text
    text = text.lower()
    text = re.sub('[^a-z0-9.]', ' ', text)
    text = ' '.join([w for w in text.split() if len(w) > 1])

    # tokenize text
    tokenized = text.split(' ')

    # remove dot (.)  if last char of token
    tokenized_aux = []
    for word in tokenized:
        if len(word) > 1:
            if (word[-1] == '.'):
                word = word[:-1]
        tokenized_aux.append(word)

    # remove stop words
    tokenized = [word for word in tokenized_aux if word not in stop_words]

    return tokenized


def match_vocabulay(lst: list, tf_idf_vectorizer):

    new_lst = []
    # check if token exist in question vocabulay, IF NOT -> discard

    for token in lst:
        if token in tf_idf_vectorizer.vocabulary_:
            new_lst.append(token)
    
    return new_lst
    