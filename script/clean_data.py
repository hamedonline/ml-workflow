# required library imports
import os
import pandas as pd


if __name__ == "__main__":

    # define relative data path (according the current path of this file)
    dirname = os.path.dirname(__file__)
    DATA_PATH = dirname+'/data/'

    df_train_full = pd.read_csv(DATA_PATH+'train.csv.gz')
    df_test = pd.read_csv(DATA_PATH+'test.csv.gz')

    # specify feature groups & target column
    features_numerical   = [column for column in df_train_full if column.startswith('cont')]
    features_categorical = [column for column in df_train_full if column.startswith('cat')]
    column_target = 'loss'

    # drop features we found during EDA
    very_highly_skewed = ['cat15', 'cat22', 'cat55', 'cat56', 'cat62', 'cat63', 'cat64', 'cat68', 'cat70']
    highly_correlated_numerical = ['cont12']
    highly_correlated_categorical = ['cat3', 'cat7']

    features_to_drop = highly_correlated_numerical + highly_correlated_categorical + very_highly_skewed

    # drop candidate features from both train & test dataframes
    df_train_full = df_train_full.drop(features_to_drop, axis=1).reset_index(drop=True)
    df_test = df_test.drop(features_to_drop, axis=1).reset_index(drop=True)


    # remove outlier samples
    df_train_full = df_train_full.drop(df_train_full[df_train_full['cont9']  < 0.05742].index).reset_index(drop=True)
    df_train_full = df_train_full.drop(df_train_full[df_train_full['cont10'] > 0.95643].index).reset_index(drop=True)

    # save cleaned data
    df_train_full.to_csv(DATA_PATH+'train_cleaned.csv.gz', compression='gzip', index=False)
    df_test.to_csv(DATA_PATH+'test_cleaned.csv.gz', compression='gzip', index=False)