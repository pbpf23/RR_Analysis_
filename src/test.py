import pytest
import pandas as pd
import datatest as dt
from datatest import (ValidationError)


def load_df(path):
    return pd.read_excel(path)  # Returns DataFrame.


def test_df_type(data):
    assert isinstance(data, pd.DataFrame)


@pytest.mark.mandatory
def test_column_names(data, required_names):
    try:
        dt.validate(data.columns, required_names)
    except ValidationError as e:
        if not all([isinstance(x, dt.differences.Extra) for x in e.differences]):
            raise e


def test_nan(data):

    subset = data.loc[:, data.columns != 'content']
    nan_subset = subset.isna().any()
    assert not nan_subset.any(), nan_subset


def test_a(data):

    requirement = {'reviews', 'translated', 'cleaned_data', 'sentiment', 'date'}
    dt.validate(data['reviews'], requirement)


def test_category_subcategory(data):

    if 'category' in data.columns:
        category = load_df("../categories.xlsx")
        test_column_names(category, {'category'})
        unique_categories_df = data['category'].unique()
        unique_categories = category['category'].unique()
        assert list(set(unique_categories_df)) == list(set(unique_categories)), f'Different categories in category file {unique_categories} and df {unique_categories_df}'
        if 'subcategory' in data.columns:
            test_column_names(category, {'subcategory'})
            unique_subcategories_df = data['subcategory'].unique()
            unique_subcategories = category['subcategory'].unique()
            assert list(set(unique_subcategories_df)) == list(
                set(unique_subcategories)), f'Different categories in category file {unique_subcategories} and df {unique_subcategories_df} '
    elif 'category' not in data.columns and 'subcategory' in data.columns:
        raise Exception('When subcategory in columns, category should be there also')


def test_output_data(data):

    if 'category' in data.columns:
        category = load_df("../brief_template.xlsx")
        test_column_names(category, {'category'})
        unique_categories_df = data['category'].unique()
        unique_categories = category['category'].unique()
        assert list(set(unique_categories_df)) == list(set(unique_categories)), f'Different categories in category file {unique_categories} and df {unique_categories_df}'
        if 'subcategory' in data.columns:
            test_column_names(category, {'subcategory'})
            unique_subcategories_df = data['subcategory'].unique()
            unique_subcategories = category['subcategory'].unique()
            assert list(set(unique_subcategories_df)) == list(
                set(unique_subcategories)), f'Different categories in category file {unique_subcategories} and df {unique_subcategories_df} '
    elif 'category' not in data.columns and 'subcategory' in data.columns:
        raise Exception('When subcategory in columns, category should be there also')


def test_input_dats(data):

    if 'category' in data.columns:
        category = load_df("../results_analysis.xlsx")
        test_column_names(category, {'category'})
        unique_categories_df = data['category'].unique()
        unique_categories = category['category'].unique()
        assert list(set(unique_categories_df)) == list(set(unique_categories)), f'Different categories in category file {unique_categories} and df {unique_categories_df}'
        if 'subcategory' in data.columns:
            test_column_names(category, {'subcategory'})
            unique_subcategories_df = data['subcategory'].unique()
            unique_subcategories = category['subcategory'].unique()
            assert list(set(unique_subcategories_df)) == list(
                set(unique_subcategories)), f'Different categories in category file {unique_subcategories} and df {unique_subcategories_df} '
    elif 'category' not in data.columns and 'subcategory' in data.columns:
        raise Exception('When subcategory in columns, category should be there also')


if __name__ == '__main__':

    df = load_df('../blush.xlsx')
    test_df_type(df)
    test_column_names(df, {'asin', 'content', 'date', 'brand'})
    test_nan(df)
    test_category_subcategory(df)
