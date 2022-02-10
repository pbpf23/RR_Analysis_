from src.cleaning_data import normalize_text
from src.detect_language import get_language
from src.labeling import label_reviews, get_labels_count, most_common
from src.statistics import save_stats
import pandas as pd
import nltk

if __name__ == '__main__':

    project_name = 'Rimmel'

    data = pd.read_excel('C:/Users/p.bozek/Downloads/RR_ANALYSIS-master/blush.xlsx')
    print(data.head())
    dictionary = pd.read_excel('C:/Users/p.bozek/Downloads/RR_ANALYSIS-master/analysis_notebook/cleaned_dict.xlsx')
    print(dictionary)

    data, eng_data, non_eng_data = get_language(data, column_name='content')
    print(eng_data.head(), non_eng_data.head())

    # TODO: Here is the place for reviews translation and mergin data.

    cleaned_data = normalize_text(eng_data, column_name='content')
    cleaned_data.to_excel(f'cleaned_data_{project_name}.xlsx')
    print('Data is cleaned')

    cleaned_data['tokens'] = cleaned_data.apply(lambda row: nltk.word_tokenize(row['lemmatized_content']), axis=1)

    # most_common_words = most_common(cleaned_data['tokens'], 1, 5)
    # print(most_common_words)

    dictionary_label_count = get_labels_count(cleaned_data, dictionary)
    dictionary_label_count.to_excel(f'dictionary_label_count_{project_name}.xlsx')
    print(dictionary_label_count.head())

    labeled_data = label_reviews(dictionary, cleaned_data, 'lemmatized_content')
    print(labeled_data.head())
    labeled_data.to_excel(f'labeled_data_{project_name}.xlsx')
    print('Data is labeled')

    statistics = save_stats(labeled_data)

    def multiple_dfs(df_list, sheets, file_name, spaces):
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
        row = 0
        for dataframe in df_list:
            dataframe.to_excel(writer, sheet_name=sheets, startrow=row, startcol=0)
            row = row + len(dataframe.index) + spaces + 1
        writer.save()

    multiple_dfs(statistics, 'Statistics', f'Statistics_{project_name}.xlsx', 1)
    print('Statistics are ready')

