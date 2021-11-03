# required library imports & initial settings

import os
import string
import random
import pickle
import numpy as np
import pandas as pd
import xgboost as xgb

from datetime import datetime
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, MinMaxScaler, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


# set seed value for reproducibility
RANDOM_SEED = 1024

# enable GPU utilization
use_gpu = True  # set this to False if your GPU is not compatible or a GPU error rises during training

# create model bin file after training
model_file_saving = True

# # create test predictions csv file
# test_predictions_saving = True

# define relative data path (according the current path of this file)
dirname = os.path.dirname(__file__)
DATA_PATH  = dirname+'/data/'
MODEL_PATH = dirname+'/model/'
MODEL_NAME_PREFIX = 'model_pipeline'


# create a unique identifier for run
unique_run_identifier = ''.join([
    datetime.now().strftime('%Y.%m.%d-%H%M%S-'),
    ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
])


# logarithmic transform function
def log_transform(value):
    return np.log1p(value)


if __name__ == "__main__":
    print('\nReading data...')
    # read data into pandas dataframes
    df_train_full = pd.read_csv(DATA_PATH+'train_cleaned.csv.gz')
    df_test = pd.read_csv(DATA_PATH+'test_cleaned.csv.gz')
    name_of_target_column = 'loss'
    name_of_target_column_transformed = name_of_target_column+'_transformed'

    # specify feature groups & target column
    features_numerical   = [column for column in df_train_full if column.startswith('cont')]
    features_categorical = [column for column in df_train_full if column.startswith('cat')]
    features_all = features_numerical + features_categorical

    print('\nProcessing data...')

    # create a new logarithmically transformed target column
    df_train_full[name_of_target_column_transformed] = df_train_full.apply(
        lambda row: log_transform(row[name_of_target_column]), axis=1)

    # let's shuffle the whole dataframe
    df_train_full = df_train_full.sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)
    # second shuffle with an exponential random seed :D
    df_train_full = df_train_full.sample(frac=1, random_state=(RANDOM_SEED**2)).reset_index(drop=True)

    # preparing requirements for numerical features
    gaussian_like = ['cont1', 'cont2', 'cont3', 'cont6', 'cont7', 'cont9', 'cont11', 'cont12']
    non_gaussian_like = ['cont4', 'cont5', 'cont8', 'cont10', 'cont13', 'cont14']
    features_numerical_to_normalize   = [column for column in gaussian_like if column in df_train_full.columns.to_list()]
    features_numerical_to_standardize = [column for column in non_gaussian_like if column in df_train_full.columns.to_list()]

    # preparing requirements for categorical features
    features_categorical_to_ordinal = list()
    features_categorical_to_onehot  = list()
    for column, variety in df_train_full[features_categorical].nunique().iteritems():
        if variety < 10: features_categorical_to_onehot.append(column)
        else: features_categorical_to_ordinal.append(column)

    # create transform pipeline for numerical features
    transformer_numerical = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('normalizer', MinMaxScaler()),
        ('standardizer', StandardScaler()),
    ])

    # create transform pipelines for categorical features
    transformer_categorical_1 = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('ordinal', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)),
        ('normal',  MinMaxScaler()),
    ])
    transformer_categorical_transformer2 = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse=False))
    ])

    # bundle preprocessing for numerical and categorical data
    preprocessor = ColumnTransformer(
        transformers=[
            ('num',  transformer_numerical, features_numerical),
            ('cat1', transformer_categorical_1, features_categorical_to_ordinal),
            ('cat2', transformer_categorical_transformer2,
            features_categorical_to_onehot),
        ])

    # create model inputs
    X_train = df_train_full[features_all]
    y_train = df_train_full[name_of_target_column_transformed].to_numpy()
    X_test  = df_test[features_all]

    tree_method_applied = 'gpu_hist' if use_gpu else 'auto'

    # xgboost hyperparameters (tuned previously)
    xgb_params = {
        'n_estimators': 35,
        'max_depth': 4,
        'eta': 0.27,

        'objective': 'reg:squarederror',
        'nthread': -1,
        'tree_method': tree_method_applied,

        'seed': RANDOM_SEED,
    }

    print('\nTraining the model...')

    # create pipeline & train
    model_xgb = xgb.XGBRegressor(**xgb_params)
    pipeline_final = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model_xgb)
    ])
    pipeline_final.fit(X_train, y_train)

    print('\nTraining completed successfully.')


    # save model bin file for inference
    if model_file_saving:
        pipeline_name = f'{MODEL_NAME_PREFIX}_{unique_run_identifier}.bin'
        with open(MODEL_PATH+pipeline_name, 'wb') as output_file:
            pickle.dump((pipeline_final), output_file)
            print(f'\nModel pipeline file saved successfully in >> {MODEL_PATH+pipeline_name}')
        output_file.close()

    # # make predictions on test data
    # y_pred_test = np.expm1(pipeline_final.predict(X_test))

    print('\\nAll done :)')
