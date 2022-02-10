import pandas as pd


def set_sentiment(row):
    if row['stars'] <= 3:
        val = 'negative'
    elif row['stars'] > 3:
        val = 'positive'
    else:
        val = 'positive'
    return val


def group_and_count(df, parameters):
    """
    df - main dataframe
    parameters = [] | a list with parameters to aggregate
    """
    df_general = df[parameters]
    parameters.remove('translated')
    df_general_first = df_general.groupby(parameters).count()
    return df_general_first


def count_total(df):
    """
    counting totals
    """
    df.loc['Total', :] = df.sum().values
    return df


def percentages_from_column(df, data_column, new_column):
    """
    column_name - new column that will be created with percentages
    """
    df[new_column] = round((df[data_column]/df['translated'].sum()) * 100, 2)
    df = count_total(df)
    df[new_column] = df[new_column].map("{:,.2f}%".format)
    return df


def drop_n_raws(df, n):
    """
    n = int - number of raws from the bottom to drop
    """
    df.drop(df.tail(1).index, inplace=True)
    return df


def topics_columns(df, column_index):
    """
    column_index - index of columns for topics counted from the end
    """
    df = df.iloc[:, column_index:]
    return df


def group_and_sum(df, parameters, aggregation_columns):
    """
    df - main dataframe
    parameters = [] | a list with parameters to aggregate
    """
    df = df.groupby(parameters)[aggregation_columns].sum()
    return df


def percentages_for_topics(df_topic_sentiment, df_topic, index_num):
    """
    index_num - number that shows how to split the data
    """
    df_topic_sentiment_negative = df_topic_sentiment.iloc[::index_num]
    df_topic_sentiment_positive = df_topic_sentiment.iloc[1::index_num]
    df_common_negative = round(df_topic_sentiment_negative/df_topic * 100, 2)
    df_common_positive = round(df_topic_sentiment_positive/df_topic * 100, 2)
    main = df_common_positive.append(df_common_negative).sort_index()
    for column in main.columns:
        main[column] = main[column].map("{:,.2f}%".format)
    main = main.replace('nan%', '0.00%')
    return main


def get_statistics_column(data, category_column, cleaned_reviews):

    # first DF
    new_column = 'content_percentages'
    data['sentiment'] = data.apply(set_sentiment, axis=1)
    parameters = [category_column, cleaned_reviews, 'sentiment']
    df_1 = group_and_count(data, parameters)
    df_1 = percentages_from_column(df_1, data_column=cleaned_reviews, new_column=new_column)

    # second DF
    df_1 = drop_n_raws(df_1, 1)
    per_category = df_1.sum(level=0, axis=0)
    category_percentage = percentages_from_column(df=per_category, data_column=cleaned_reviews, new_column=new_column)
    print(percentages_from_column)

    # third DF
    per_sentiment = df_1.sum(level=1, axis=0)
    sentiment_percentage = percentages_from_column(df=per_sentiment, data_column=cleaned_reviews, new_column=new_column)
    print(percentages_from_column)
    return df_1, category_percentage, sentiment_percentage


def get_stats_topics(data):
    cleaned_date = []
    for one_date in data['date']:
        length_date = len(one_date.split(" "))
        split_date = one_date.split(" ")[length_date - 1]
        cleaned_date.append(split_date)
    data["year"] = cleaned_date

    df_topics_names = topics_columns(data, -23)
    df_topic_sentiment = group_and_sum(data, parameters=['category', 'sentiment'], agregation_columns=df_topics_names.columns)
    df_topic = group_and_sum(data, parameters=['category'], agregation_columns=df_topics_names.columns)
    df_topic_in_percentage = percentages_for_topics(df_topic_sentiment, df_topic, index_num=2)

    # HISTORICSAL DATA FOR GRAPHS
    df_historical_per_market = group_and_sum(data, parameters=['category', 'sentiment', 'year'], agregation_columns=df_topics_names.columns)
    return data, df_topic_in_percentage, df_historical_per_market


def percentChange(df, raws_num, itter_star=0):
    df_main = df.iloc[int(itter_star):int(raws_num)].pct_change(periods= 1)
    for itter_num in range(round(df.shape[0]/raws_num) - 1):
        itter_star = itter_star + raws_num
        df_part = df.iloc[itter_star:(raws_num + itter_star)].pct_change(periods= 1)
        df_main = df_main.append(df_part)
        df_main = df_main.round(4)
    return df_main.multiply(100)


def percentage_sign(df):
    for column in df.columns:
        df[column] = df[column].map("{:,.2f}%".format)
        df = df.replace('nan%', '-')
        df = df.replace('inf%', '-')
    return df


def get_data_stats(df_historical_per_market):
    # # RUN
    df_historical_per_market_percents = percentChange(df_historical_per_market, raws_num=3, itter_star=0)
    df_historical_per_market_percents_ = percentage_sign(df_historical_per_market_percents)
    return df_historical_per_market_percents_


def save_stats(df):

    # first DF
    parameters = ['category', 'cleaned_content', 'sentiment']
    df_1 = group_and_count(df, parameters)
    df_1 = percentages_from_column(df_1, data_column='cleaned_content', new_column='content_percentages')

    # second DF
    df_1 = drop_n_raws(df_1, 1)
    per_category = df_1.sum(level=0, axis=0)
    percentages_from_column(df=per_category, data_column='cleaned_content', new_column='content_percentage')

    # third DF
    per_sentiment = df_1.sum(level=1, axis=0)
    percentages_from_column(df=per_sentiment, data_column='cleaned_content', new_column='content_percentage')

    # stats per topic
    df_topics_names = topics_columns(df, -23)
    df_topic_sentiment = group_and_sum(df, parameters=['category', 'sentiment'], agregation_columns=df_topics_names.columns)
    df_topic = group_and_sum(df, parameters=['category'], agregation_columns=df_topics_names.columns)
    df_topic_in_percentage = percentages_for_topics(df_topic_sentiment, df_topic, index_num=2)

    # HISTORICSAL DATA FOR GRAPHS
    df_historical_per_market = group_and_sum(df, parameters=['category', 'sentiment', 'year'], agregation_columns=df_topics_names.columns)
    df_historical_per_market_percents = percentChange(df_historical_per_market, raws_num=3, itter_star=0)
    df_historical_per_market_percents = percentage_sign(df_historical_per_market_percents)

    fin_data = [df_1, per_category, per_sentiment, df_topic_in_percentage, df_topic_sentiment, df_topic, df_historical_per_market_percents, df_historical_per_market]

    return fin_data
