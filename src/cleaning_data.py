import string
import pandas as pd
import nltk
import re
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('wordnet')


def content_cleaner(text: str) -> str:
    """
    :param text:
    :return:
    """
    try:
        return str(text)
    except ValueError:
        return str('nan')


def number_cleaner(text) -> int or float:
    """
    :param text:
    :return:
    """
    try:
        return int(text)
    except ValueError:
        return float(text)


def lowercase(text: str) -> str:
    """
    Lowercase text.
    :param text:
    :return: str
    """
    return text.lower()


def remove_punctuation(text: str) -> str:
    """
    Replace punctuations from text with whitespaces.
    :param text: raw text
    :return: str
    """
    return re.sub(r"[^\w\s]", '', text)


def remove_unicode(text: str) -> str:
    """
    :param text: str
    :return: str
    """
    return text.encode('ascii', 'ignore').decode()


def remove_stopwords(text: str) -> str:
    """
    Remove stop words from text.
    :param text: str
    :return: str
    """
    stop_words = stopwords.words("english")
    return ' '.join([word for word in text.split(' ') if word not in stop_words])


def remove_mentions(text: str) -> str:
    """
    :param text:
    :return: str
    """
    return re.sub("@\S+", " ", text)


def remove_url(text: str) -> str:
    """
    Remove urls from text.
    :param text: raw text
    :return: str
    """
    return re.sub("https*\S+", " ", text)


def remove_hashtags(text: str) -> str:
    """
    Remove hashtags from text.
    :param text: raw text
    :return: str
    """
    return re.sub("#\S+", " ", text)


def remove_ticks(text: str) -> str:
    """
    Remove ticks from text.
    :param text: raw text
    :return: str
    """
    return re.sub("\'\w+", '', text)


def remove_numbers(text: str) -> str:
    """
    Remove numbers from text and words with numbers.
    :param text: raw text
    :return: str
    """
    return re.sub(r'\w*\d+\w*', '', text)


def remove_extra_space(text: str) -> str:
    """
    Remove over spaces from text.
    :param text: raw text
    :return: str
    """
    return re.sub(' +', ' ', text)


def words_limit(text: str) -> str:
    """
    Remove data that got less words then 3.
    :param text: dataframe
    :return: str
    """
    return re.sub(r'\b\w{1,3}\b', ' ', text)


def stem_words(data) -> str:
    """
    Stem words in list of tokenized words.
    :param data: dataframe
    :return: str
    """
    stemmer = PorterStemmer()
    stems = []
    words = word_tokenize(data)
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return " ".join(stems)


def tokenize(text):
    """
    Tokenize text.
    :param text: str
    :return: str
    """
    tokenized = word_tokenize(text)
    no_punc = []
    for review in tokenized:
        line = "".join(char for char in review if char not in string.punctuation)
        no_punc.append(line)
    tokens = lemmatize(no_punc)
    return tokens


def lemmatize(tokens):
    """
    Lemmatize tokens.
    :param tokens: str
    :return: str
    """
    lmtzr = WordNetLemmatizer()
    lemma = [lmtzr.lemmatize(t) for t in tokens]
    return " ".join(lemma)


def get_date(data, country, date_column) -> pd.DataFrame:
    """
    Clean data and leave only a year.
    :param date_column:
    :param country: str
    :param data: raw dataframe
    :return: dataframe
    """
    if country == 'co.uk' or 'us':
        data[date_column] = data[date_column].apply(lambda x: x.split('on ')[-1])
    if country == 'fr':
        data[date_column] = data[date_column].apply(lambda x: x.split('le ')[-1])
    if country == 'it':
        data[date_column] = data[date_column].apply(lambda x: x.split('il ')[-1])
    if country == 'es':
        data[date_column] = data[date_column].apply(lambda x: x.split('el ')[-1])
    if country == 'de':
        data[date_column] = data[date_column].apply(lambda x: x.split('de ')[-1])

    data[date_column] = pd.to_datetime(data[date_column]).dt.strftime('%Y')
    return data


def remove_old_data(data, date_column, year) -> pd.DataFrame:
    data[date_column] = data[date_column].map(number_cleaner)
    return data[data[date_column] > year]


def clean_data(data, column_name) -> pd.DataFrame:
    """
    Removing unnecessary elements from the text that hinder the analysis.
    :param column_name: string reviews
    :param data: dataframe
    :return: dataframe
    """
    data.drop_duplicates(inplace=True)
    data.reset_index(inplace=True)
    print(f'This is data before cleaning: {data[column_name][0]}')
    data[column_name] = data[column_name].map(content_cleaner)
    data[column_name] = data[column_name].map(remove_url)
    data[column_name] = data[column_name].map(remove_mentions)
    data[column_name] = data[column_name].map(remove_unicode)
    data[column_name] = data[column_name].map(remove_hashtags)
    data[column_name] = data[column_name].map(remove_ticks)
    data[column_name] = data[column_name].map(remove_numbers)
    data[column_name] = data[column_name].map(remove_extra_space)
    data[column_name] = data[column_name].map(remove_punctuation)
    data[column_name] = data[column_name].map(lowercase)
    # data[column_name] = data[column_name].map(remove_brands)
    # data[column_name] = data[column_name].map(words_limit)
    print(f'This is data after cleaning: {data[column_name][0]}')

    return data


def remove_brands(data):
    brand_list = ['max factor', 'rimmel']
    for brand in brand_list:
        data = data[~data['brand'].str.contains(str(brand))]
    return data


def normalize_text(data, column_name):
    """
    Stemming and/or Leammatization after stop words removal.
    :param data: dataframe
    :param column_name: string reviews
    :return: dataframe
    """
    data_cleaned = clean_data(data, column_name)
    data_cleaned['no_stopwords_content'] = data_cleaned[column_name].map(remove_stopwords)
    data_cleaned['stemmed_content'] = data_cleaned['no_stopwords_content'].map(stem_words)
    data_cleaned['lemmatized_content'] = data_cleaned['no_stopwords_content'].apply(lambda x: tokenize(x))
    print(f'This is data without stopwords: {data["no_stopwords_content"][0]}')
    print(f'This is stemmed data: {data["stemmed_content"][0]}')
    print(f'This is lemmatized data: {data["lemmatized_content"][0]}')

    return data_cleaned


def clean_date(data, date_column):
    year = '2016'
    country = data.country[0]
    data = get_date(data, country, date_column)
    data = remove_old_data(data, date_column, year)
    return data
