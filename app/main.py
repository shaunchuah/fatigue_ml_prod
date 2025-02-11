from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, SQLModel, create_engine, func, select

from app.config import Settings
from app.ml_services import (
    generate_force_plot,
    load_ml_resources,
    prepare_dataframe,
)
from app.models import Input, InputData
from app.utils import (
    format_for_database,
    format_input_data,
)

settings = Settings()

app = FastAPI()

input_data_model = InputData()
database_url = settings.database_url
engine = create_engine(database_url, echo=True)


SQLModel.metadata.create_all(engine)


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
    return {
        "Project": "IBD Fatigue ML API",
        "Version": "0.1.0",
        "Author": "Shaun Chuah",
    }


@app.get("/analytics")
def analytics():
    with Session(engine) as session:
        # get count
        count = session.exec(select(func.count(InputData.id))).all()

    return {
        "API access count": count[0],
    }


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

        # Store formatted_data_dictionary in database
        formatted_data_db_storage = format_for_database(formatted_data_dictionary)
        input_data = InputData(
            **formatted_data_db_storage,
            predicted_class=predicted_class,
            predicted_probability=predicted_probability,
        )
        session = Session(engine)
        session.add(input_data)
        session.commit()

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
