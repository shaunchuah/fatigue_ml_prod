from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.models import Input
from src.utils import (
    format_input_data,
    generate_force_plot,
    load_ml_resources,
    prepare_dataframe,
)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://musicstudy.uk",
    "https://www.musicstudy.uk",
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
        formatted_data_dictionary = format_input_data(input)
        df = prepare_dataframe(formatted_data_dictionary, scaler)
        predicted_probability = model.predict(df)[0][0].item()
        predicted_class = "fatigue" if predicted_probability > 0.5 else "no_fatigue"
        base64_image = generate_force_plot(df, scaler)

        return {
            "predicted_class": predicted_class,
            "predicted_probability": predicted_probability,
            "force_plot": base64_image,
            "prediction_data": formatted_data_dictionary,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
