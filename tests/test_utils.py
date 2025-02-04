import datetime
import math

from app.models import Input
from app.utils import calculate_bmi, calculate_disease_duration, format_input_data


def test_calculate_bmi():
    height = 180.0
    weight = 80.0
    expected_bmi = weight / ((height / 100) ** 2)
    result = calculate_bmi(height, weight)
    assert math.isclose(result, expected_bmi, rel_tol=1e-5)


def test_calculate_disease_duration():
    today = datetime.date.today()
    days_ago = 21  # 3 weeks ago
    diagnosis_date = today - datetime.timedelta(days=days_ago)
    expected_weeks = days_ago / 7
    result = calculate_disease_duration(diagnosis_date)
    assert math.isclose(result, expected_weeks, rel_tol=1e-5)


def test_format_input_data():
    # Set up a dummy input with fixed values.
    today = datetime.date.today()
    diagnosis_date = today - datetime.timedelta(days=35)  # 5 weeks ago

    input_data = Input(
        height=160.0,
        weight=64.0,
        date_of_diagnosis=diagnosis_date,
        study_group="ibdu",
        age=40,
        sex=0,
        age_at_diagnosis=35,
        montreal_upper_gi=0,
        montreal_perianal=0,
        albumin=4.0,
        crp=1.0,
        haemoglobin=14.0,
        red_cell_count=5.0,
        white_cell_count=7.0,
        neutrophils=4.0,
        lymphocytes=3.0,
        monocytes=0.5,
        eosinophils=0.2,
        basophils=0.1,
        platelets=250,
        urea=30.0,
        creatinine=1.0,
        sodium=140,
        potassium=4.0,
        calprotectin=50,
        sampling_steroids=0,
        sampling_abx=0,
        sampling_asa=0,
        sampling_aza=0,
        sampling_mp=0,
        sampling_ifx=0,
        sampling_ada=0,
        sampling_vedo=0,
        sampling_uste=0,
        sampling_tofa=0,
        sampling_mtx=0,
        sampling_ciclosporin=0,
        sampling_filgo=0,
        sampling_upa=0,
        sampling_risa=0,
        montreal_cd_location="l1",
        montreal_cd_behaviour="b3",
        montreal_uc_extent="e3",
        montreal_uc_severity="s3",
        is_smoker="Ex-smoker",
    )

    # Get the formatted data
    result = format_input_data(input_data)

    # Expected calculated fields
    expected_diagnosis_year = input_data.date_of_diagnosis.year

    # Determine expected season flags
    month = today.month
    if month in (12, 1, 2):
        exp_season_winter, exp_season_spring, exp_season_summer, exp_season_autumn = (
            1,
            0,
            0,
            0,
        )
    elif month in (3, 4, 5):
        exp_season_winter, exp_season_spring, exp_season_summer, exp_season_autumn = (
            0,
            1,
            0,
            0,
        )
    elif month in (6, 7, 8):
        exp_season_winter, exp_season_spring, exp_season_summer, exp_season_autumn = (
            0,
            0,
            1,
            0,
        )
    else:
        exp_season_winter, exp_season_spring, exp_season_summer, exp_season_autumn = (
            0,
            0,
            0,
            1,
        )

    # Basic field validations
    assert result["diagnosis_year"] == expected_diagnosis_year
    assert result["age"] == 40
    assert result["sex"] == 0
    assert result["height"] == 160.0
    assert result["weight"] == 64.0
    assert result["age_at_diagnosis"] == 35

    # Study group mapping (ibdu)
    assert result["study_group_name_IBDU"] == 1
    assert result["study_group_name_CD"] == 0
    assert result["study_group_name_UC"] == 0

    # Montreal mappings
    # For montreal_cd_location: "l1" should yield L1 Ileal = 1
    assert result["montreal_cd_location_L1 Ileal"] == 1
    assert result["montreal_cd_location_L2 Colonic"] == 0
    assert result["montreal_cd_location_L3 Ileocolonic"] == 0
    # For montreal_cd_behaviour: "b3" should yield B3 Penetrating = 1
    assert result["montreal_cd_behaviour_B1 Non-stricturing, non-penetrating"] == 0
    assert result["montreal_cd_behaviour_B2 Stricturing"] == 0
    assert result["montreal_cd_behaviour_B3 Penetrating"] == 1
    # For montreal_uc_extent: "e3" should yield E3 Extensive = 1
    assert result["montreal_uc_extent_E1 Proctitis"] == 0
    assert result["montreal_uc_extent_E2 Left-sided"] == 0
    assert result["montreal_uc_extent_E3 Extensive"] == 1
    # For montreal_uc_severity: "s3" should yield S3 Severe = 1
    assert result["montreal_uc_severity_S0 Remission"] == 0
    assert result["montreal_uc_severity_S1 Mild"] == 0
    assert result["montreal_uc_severity_S2 Moderate"] == 0
    assert result["montreal_uc_severity_S3 Severe"] == 1

    # Smoking mapping ("Ex-smoker")
    assert result["is_smoker_Ex-smoker"] == 1
    assert result["is_smoker_Non-smoker"] == 0
    assert result["is_smoker_Smoker"] == 0

    # Season mapping assertions
    assert result["season_winter"] == exp_season_winter
    assert result["season_spring"] == exp_season_spring
    assert result["season_summer"] == exp_season_summer
    assert result["season_autumn"] == exp_season_autumn
