from langdetect import detect


def detect_language(data, column_name) -> list:
    """
    Detect language with detect. Creates column with language info.
    :param column_name:
    :param data: dataframe
    :return: list
    """
    detected_lang = []

    for i, row in enumerate(data[column_name]):
        try:
            value = detect(row)
        except Exception as e:
            print(e)
            value = None
        detected_lang.append(value)

    return detected_lang


def get_language(data, column_name):
    data['language'] = detect_language(data, column_name)

    eng_data = data[data.language == 'en']
    eng_data.reset_index(inplace=True)

    foreign_data = data[data.language != 'en']
    foreign_data.reset_index(inplace=True)

    return data, eng_data, foreign_data
