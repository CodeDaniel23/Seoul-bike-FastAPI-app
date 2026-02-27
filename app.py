from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
import pickle

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

model = pickle.load(open("seoul_data.pkl", "rb"))


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
def predict(
    request: Request,
    hour: int = Form(...),
    temperature: float = Form(...),
    humidity: float = Form(...),
    wind_speed: float = Form(...),
    visibility: float = Form(...),
    solar_radiation: float = Form(...),
    rain_fall: float = Form(...),
    snow_fall: float = Form(...),
    seasons: str = Form(...),
    holidays: str = Form(...),
    functioning_day: str = Form(...),
    year: int = Form(...),
    month: int = Form(...),
    day: int = Form(...),
    week_day: int = Form(...)
):

    input_data = pd.DataFrame([{
        "Hour": hour,
        "Temperature(°C)": temperature,
        "Humidity(%)": humidity,
        "Wind speed (m/s)": wind_speed,
        "Visibility (10m)": visibility,
        "Solar Radiation (MJ/m2)": solar_radiation,
        "Rainfall(mm)": rain_fall,
        "Snowfall (cm)": snow_fall,
        "Seasons": seasons,
        "Holiday": holidays,
        "Functioning Day": functioning_day,
        "year": year,
        "month": month,
        "day": day,
        "weekday": week_day
    }])

    prediction = model.predict(input_data)[0]

    numerical_prediction = int(prediction)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "prediction_text": f"Estimated Bike demand: {numerical_prediction}"
        }
    )