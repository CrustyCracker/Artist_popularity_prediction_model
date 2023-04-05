from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse, Response
from copy import deepcopy
import matplotlib.pyplot as plt
import pickle as pkl
import pandas as pd
import uvicorn
import json
import io
import os
plt.rcParams["figure.figsize"] = (20, 10)
app = FastAPI()


class NaiveModel:
    def __init__(self, data):
        self.data = data

    def predict(self, months: int):
        if months < 1:
            raise ValueError('months must be greater than 0')
        if months == 1:
            return self.data[-1]

        return [self.data[-1] for _ in range(months)]


def get_predictions(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def save_predictions(filename, previous_data, model, artist, actual, predicted):
    to_save = {
        "model": model,
        "artist": artist,
        "actual": actual,
        "predicted": int(predicted),
        "mean": abs(actual - int(predicted))
    }
    previous_data.append(to_save)
    with open(filename, 'w') as f:
        json.dump(previous_data, f, indent=4)


def date_to_month(date):
    return date.strftime('%Y-%m')


def generate_plot_buf(data, arima_pred, naive_pred, arima_to_plot, naive_to_plot, artist_name):
    plt.title(f'Predictions for {artist_name}')
    plt.locator_params(axis='y', nbins=20)
    plt.xticks(rotation=270)
    plt.plot(data, label="Real data" , marker='o', markersize=3, color='black')
    plt.plot(arima_to_plot, marker='o', markersize=3, label="ARIMA prediction", color='green')
    plt.plot(naive_to_plot, marker='o', markersize=3, label="Naive prediction", color='red')

    plt.plot([data.index[-1], arima_to_plot.index[0]], [data[-1], arima_pred[0]], color='green', linestyle='-', linewidth=2)
    plt.plot([data.index[-1], naive_to_plot.index[0]], [data[-1], naive_pred[0]], color='red', linestyle='-', linewidth=2)

    plt.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf


@app.get("/", response_class=PlainTextResponse)
def root():
    return """To run prediction by specific model to specific artist go to /predict/[model_name]/[artist_name]

To create plot with predictions for specific artist go to /predict_plot/[artist_name]

To read collected data for a/b test go to /test_ab"""


@app.get("/predict/{model_name}/{artist_name}", response_class=PlainTextResponse)
async def predict(model_name: str, artist_name: str):
    if model_name not in models.keys():
        raise HTTPException(status_code=404, detail=f'Model {model_name} does not exist.')
    elif artist_name not in models[model_name].keys():
        raise HTTPException(status_code=404, detail=f'Artist {artist_name} does not exist.')

    model = models[model_name][artist_name]
    if model_name == "arima":
        prediction = model.predict(n_periods=1)[0]
    else:
        prediction = model.predict(1)

    data = deepcopy(clicks[artist_name])
    next = data.popitem()
    current = data.popitem()[1]
    previous_data = get_predictions(os.path.join(current_path, "data", "v3", "ab_test_data.json"))
    save_predictions(os.path.join(current_path, "data", "v3", "ab_test_data.json"), previous_data, model_name, artist_name, next[1], prediction)

    percentage = round((prediction - current) / current * 100, 2)
    if prediction > current:
        message = f'The popularity of {artist_name} is going to increase by {percentage}%'
    elif prediction < current:
        message = f'The popularity of {artist_name} is going to decrease by {-percentage}%'
    else:
        message = f'The popularity of {artist_name} is going to stay the same'
    return message


@app.get("/predict_plot/{artist_name}", response_class=Response)
async def predict_plot(artist_name: str):
    if artist_name not in models["arima"].keys():
        raise HTTPException(status_code=404, detail=f'Artist {artist_name} does not exist.')

    number_of_months = 12
    arima_predictions = models['arima'][artist_name].predict(n_periods=number_of_months)
    naive_predictions = models["naive"][artist_name].predict(number_of_months)

    data = deepcopy(clicks[artist_name])
    data.popitem()
    data = pd.Series(data)
    arima_predictions_to_plot = pd.Series(arima_predictions, index= date_to_month(pd.date_range(date_to_month(pd.to_datetime(data.keys()[-1]) + pd.DateOffset(months=1)), periods=number_of_months, freq='MS')))
    naive_predictions_to_plot = pd.Series(naive_predictions, index= date_to_month(pd.date_range(date_to_month(pd.to_datetime(data.keys()[-1]) + pd.DateOffset(months=1)), periods=number_of_months, freq='MS')))

    plot = generate_plot_buf(data, arima_predictions, naive_predictions, arima_predictions_to_plot, naive_predictions_to_plot, artist_name)
    return Response(content=plot.read(), media_type="image/png")


@app.get("/test_ab", response_class=PlainTextResponse)
async def test_ab():
    predictions = json.dumps(get_predictions(os.path.join(current_path, "data", "v3", "ab_test_data.json")), indent=4)
    return predictions


if __name__ == "__main__":
    current_path = os.path.dirname(__file__)
    print(current_path)

    # load models
    models = {}
    for model_name in ["naive", "arima"]:
        with open(os.path.join(current_path, "models", f'{model_name}_models.pickle'), "rb") as f:
            models_dictionary = pkl.load(f)
        models[model_name] = models_dictionary

    # load data
    with open(os.path.join(current_path, "data", "v3", "artists_clicks_per_month.json"), 'r') as f:
        clicks = json.load(f)

    uvicorn.run(app)
