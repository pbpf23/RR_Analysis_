from collections import Counter
from operator import itemgetter
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('wordnet')


def search_word(text, dictionary):
    """

    :param text:
    :param dictionary:
    :return:
    """
    return int(any(" " + str(word) + " " in text for word in dictionary))


def label_reviews(dictionary, data, cleaned_column):
    """
    Label reviews with dictionary with 0 or 1.
    :param cleaned_column:
    :param dictionary: dataframe
    :param data: dataframe
    :return: dataframe
    """
    dict_columns = dictionary.columns
    print(dict_columns)
    words_list = [dictionary[col].tolist() for col in dict_columns]
    cleaned_words_list = [[x for x in word if str(x) != 'nan'] for word in words_list]
    for column_name, cleaned_word in zip(dict_columns, cleaned_words_list):
        data[column_name] = data[cleaned_column].apply(lambda x: search_word(x, cleaned_word))
    return data


def most_common(tokens, threshold=10, how_many=1):
    """

    :param tokens:
    :param threshold:
    :param how_many:
    :return:
    """
    stop_words = stopwords.words("english")
    sorted_data = sorted(Counter(tokens).items(), key=itemgetter(1), reverse=True)
    most_common_words = [x for x in sorted_data if x[0] not in stop_words]
    if threshold:
        return [x for x in most_common_words if x[1] > threshold]
    elif how_many:
        return most_common_words


def get_labels_count(data, dictionary):
    """

    :param data:
    :param dictionary:
    :return:
    """
    content = " ".join([str(x) for x in data['tokens'].values])

    dict_columns = dictionary.columns

    for column in dict_columns:
        word_count = []
        for row in dictionary[column]:
            cnt = content.count(str(row))
            word_count.append(cnt)
        dictionary[f'{column} count'] = word_count
        dictionary = dictionary.reindex(sorted(dictionary.columns), axis=1)
    return dictionary
