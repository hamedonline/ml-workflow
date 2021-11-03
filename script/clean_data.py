# required library imports

import os
import string
import random
import pandas as pd

from datetime import datetime


# create fresh data files after cleaning
data_file_saving = True

# define relative data path (according the current path of this file)
dirname = os.path.dirname(__file__)
DATA_PATH = dirname+'/data/'


# create a unique identifier for run
unique_run_identifier = ''.join([
    datetime.now().strftime('%Y.%m.%d-%H%M%S-'),
    ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
])


if __name__ == "__main__":
    print('\nReading data...')
    # read data into pandas dataframes
    df_train_full = pd.read_csv(DATA_PATH+'train.csv.gz')
    df_test = pd.read_csv(DATA_PATH+'test.csv.gz')


    print('\nProcessing data...')

    # specify feature groups & target column
    features_numerical   = [column for column in df_train_full if column.startswith('cont')]
    features_categorical = [column for column in df_train_full if column.startswith('cat')]
    column_target = 'loss'

    # drop features we spotted as not useful during EDA
    very_highly_skewed = ['cat15', 'cat22', 'cat55', 'cat56', 'cat62', 'cat63', 'cat64', 'cat68', 'cat70']
    highly_correlated_numerical = ['cont12']
    highly_correlated_categorical = ['cat3', 'cat7']

    features_to_drop = highly_correlated_numerical + highly_correlated_categorical + very_highly_skewed

    # drop candidate features from both train & test dataframes
    df_train_full = df_train_full.drop(features_to_drop, axis=1).reset_index(drop=True)
    df_test = df_test.drop(features_to_drop, axis=1).reset_index(drop=True)


    # remove outlier samples (identified on EDA stage)
    df_train_full = df_train_full.drop(df_train_full[df_train_full['cont9']  < 0.05742].index).reset_index(drop=True)
    df_train_full = df_train_full.drop(df_train_full[df_train_full['cont10'] > 0.95643].index).reset_index(drop=True)

    print('\nData processing completed successfully.')


    if data_file_saving:
        print('\nCompressing & saving dataset files...')
        # save cleaned data
        new_train_file_name_path = f'{DATA_PATH}train_cleaned({unique_run_identifier}).csv.gz'
        new_test_file_name_path  = f'{DATA_PATH}test_cleaned({unique_run_identifier}).csv.gz'
        df_train_full.to_csv(new_train_file_name_path, compression='gzip', index=False)
        df_test.to_csv(new_test_file_name_path, compression='gzip', index=False)
        print(f'\nDataset files saved successfully in >> \n{new_train_file_name_path} \n{new_test_file_name_path}')

    print('\n\nAll done :)')