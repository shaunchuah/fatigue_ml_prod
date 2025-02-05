from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.ml_services import (
    generate_force_plot,
    load_ml_resources,
    prepare_dataframe,
)
from app.models import Input
from app.utils import (
    format_input_data,
)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://musicstudy.uk",
    "https://www.musicstudy.uk",
    "https://sampletrek.com",
    "https://edi.sampletrek.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


model, scaler = load_ml_resources()


@app.post("/predict")
def predict_fatigue(input: Input):
    try:
        import time

        timings = {}

        start = time.perf_counter()
        formatted_data_dictionary = format_input_data(input)
        timings["input_data_formatting"] = round(
            (time.perf_counter() - start) * 1000, 3
        )

        start = time.perf_counter()
        df = prepare_dataframe(formatted_data_dictionary, scaler)
        timings["dataframe_preparation"] = round(
            (time.perf_counter() - start) * 1000, 3
        )

        start = time.perf_counter()
        predicted_probability = model.predict(df)[0][0].item()
        timings["model_prediction"] = round((time.perf_counter() - start) * 1000, 3)

        predicted_class = "fatigue" if predicted_probability > 0.5 else "no_fatigue"

        start = time.perf_counter()
        base64_image = generate_force_plot(df, scaler)
        timings["force_plot_generation"] = round(
            (time.perf_counter() - start) * 1000, 3
        )

        return {
            "execution_time_ms": timings,
            "predicted_class": predicted_class,
            "predicted_probability": predicted_probability,
            "prediction_data": formatted_data_dictionary,
            "force_plot": base64_image,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
