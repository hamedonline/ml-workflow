# required library imports
import json
import pickle
from pandas import DataFrame
from numpy import expm1
from flask import Flask, request
from waitress import serve

# path to the folder containing our model
MODEL_PATH = './model/'


def load_model(path_to_model):
    with open(path_to_model, 'rb') as model_file:
        model = pickle.load(model_file)
    return model


def get_prediction(model, input_data):
    # input data is a json string
    # we have to convert it back to a pandas dataframe object
    # scikit-learn's ColumnTransformer only accepts an array or pandas DataFrame
    dict_obj = json.loads(input_data)
    X = DataFrame.from_dict(dict_obj)
    y_pred = expm1(model.predict(X)[0])

    # compose result dictionary and return it as a json string
    result = {
        'prediction': float(y_pred),
    }
    return json.dumps(result)


app = Flask('prediction_app')
@app.route('/predict', methods=['POST'])
def predict():
    input_json = request.get_json()
    model = load_model(MODEL_PATH+'model.bin')
    prediction_result = get_prediction(model, input_json)

    return prediction_result



if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=9696)