from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

sample_input = {
    "age": 40,
    "sex": 1,
    "height": 175.0,
    "weight": 70.0,
    "age_at_diagnosis": 30,
    "montreal_upper_gi": 0,
    "montreal_perianal": 1,
    "albumin": 45.0,
    "crp": 8.0,
    "haemoglobin": 150.0,
    "red_cell_count": 5.0,
    "white_cell_count": 8.0,
    "neutrophils": 5.0,
    "lymphocytes": 2.5,
    "monocytes": 0.7,
    "eosinophils": 0.3,
    "basophils": 0.1,
    "platelets": 300.0,
    "urea": 15.0,
    "creatinine": 60.0,
    "sodium": 138.0,
    "potassium": 4.2,
    "calprotectin": 120.0,
    "sampling_steroids": 1,
    "sampling_abx": 0,
    "sampling_asa": 1,
    "sampling_aza": 0,
    "sampling_mp": 0,
    "sampling_ifx": 1,
    "sampling_ada": 0,
    "sampling_vedo": 0,
    "sampling_uste": 0,
    "sampling_tofa": 0,
    "sampling_mtx": 0,
    "sampling_ciclosporin": 0,
    "sampling_filgo": 0,
    "sampling_upa": 0,
    "sampling_risa": 0,
    "date_of_diagnosis": "2015-07-15",
    "study_group": "cd",
    "montreal_cd_location": "l1",
    "montreal_cd_behaviour": "b1",
    "montreal_uc_extent": "e1",
    "montreal_uc_severity": "s0",
    "is_smoker": "Non-smoker",
}


def test_predict_endpoint():
    response = client.post("/predict", json=sample_input)
    assert response.status_code == 200, (
        f"Expected status code 200 but got {response.status_code}"
    )
    data = response.json()

    # Check response keys presence
    expected_keys = {
        "predicted_class",
        "predicted_probability",
        "force_plot",
        "prediction_data",
        "execution_time_ms",
    }
    assert expected_keys.issubset(data.keys()), (
        f"Missing keys in response: {expected_keys - data.keys()}"
    )


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
