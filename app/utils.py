import datetime

from app.models import Input


def calculate_bmi(height: float, weight: float) -> float:
    """
    Weight in kg. Height in cm.
    """
    height_in_m = height / 100
    return weight / (height_in_m**2)


def calculate_disease_duration(date_of_diagnosis: datetime.date) -> float:
    return (datetime.date.today() - date_of_diagnosis).days / 7


def format_input_data(input: Input) -> dict:
    """
    Takes web input data, formats it for ML prediction.
    Returns a formatted data dictionary
    """
    # Calculate BMI and disease duration
    bmi = calculate_bmi(input.height, input.weight)
    disease_duration_weeks = calculate_disease_duration(input.date_of_diagnosis)
    diagnosis_year = input.date_of_diagnosis.year

    # Calculate season
    month = datetime.date.today().month
    season_winter = 0
    season_spring = 0
    season_summer = 0
    season_autumn = 0

    match month:
        case 12 | 1 | 2:
            season_winter = 1
        case 3 | 4 | 5:
            season_spring = 1
        case 6 | 7 | 8:
            season_summer = 1
        case 9 | 10 | 11:
            season_autumn = 1

    # Study Group
    study_group_name_CD = 0
    study_group_name_IBDU = 0
    study_group_name_UC = 0

    match input.study_group:
        case "cd":
            study_group_name_CD = 1
        case "ibdu":
            study_group_name_IBDU = 1
        case "uc":
            study_group_name_UC = 1

    # Montreal
    montreal_cd_location_L1_Ileal = 0
    montreal_cd_location_L2_Colonic = 0
    montreal_cd_location_L3_Ileocolonic = 0
    montreal_cd_behaviour_B1_Non_stricturing_non_penetrating = 0
    montreal_cd_behaviour_B2_Stricturing = 0
    montreal_cd_behaviour_B3_Penetrating = 0
    montreal_uc_extent_E1_Proctitis = 0
    montreal_uc_extent_E2_Left_sided = 0
    montreal_uc_extent_E3_Extensive = 0
    montreal_uc_severity_S0_Remission = 0
    montreal_uc_severity_S1_Mild = 0
    montreal_uc_severity_S2_Moderate = 0
    montreal_uc_severity_S3_Severe = 0

    match input.montreal_cd_location:
        case "l1":
            montreal_cd_location_L1_Ileal = 1
        case "l2":
            montreal_cd_location_L2_Colonic = 1
        case "l3":
            montreal_cd_location_L3_Ileocolonic = 1

    match input.montreal_cd_behaviour:
        case "b1":
            montreal_cd_behaviour_B1_Non_stricturing_non_penetrating = 1
        case "b2":
            montreal_cd_behaviour_B2_Stricturing = 1
        case "b3":
            montreal_cd_behaviour_B3_Penetrating = 1

    match input.montreal_uc_extent:
        case "e1":
            montreal_uc_extent_E1_Proctitis = 1
        case "e2":
            montreal_uc_extent_E2_Left_sided = 1
        case "e3":
            montreal_uc_extent_E3_Extensive = 1

    match input.montreal_uc_severity:
        case "s0":
            montreal_uc_severity_S0_Remission = 1
        case "s1":
            montreal_uc_severity_S1_Mild = 1
        case "s2":
            montreal_uc_severity_S2_Moderate = 1
        case "s3":
            montreal_uc_severity_S3_Severe = 1

    # Smoking
    is_smoker_Ex_smoker = 0
    is_smoker_Non_smoker = 0
    is_smoker_Smoker = 0

    match input.is_smoker:
        case "Ex-smoker":
            is_smoker_Ex_smoker = 1
        case "Non-smoker":
            is_smoker_Non_smoker = 1
        case "Smoker":
            is_smoker_Smoker = 1

    # Format the data
    formatted_data_dictionary = {
        "has_active_symptoms": input.has_active_symptoms,
        "age": input.age,
        "sex": input.sex,
        "height": input.height,
        "weight": input.weight,
        "bmi": bmi,
        "age_at_diagnosis": input.age_at_diagnosis,
        "montreal_upper_gi": input.montreal_upper_gi,
        "montreal_perianal": input.montreal_perianal,
        "albumin": input.albumin,
        "crp": input.crp,
        "haemoglobin": input.haemoglobin,
        "red_cell_count": input.red_cell_count,
        "white_cell_count": input.white_cell_count,
        "neutrophils": input.neutrophils,
        "lymphocytes": input.lymphocytes,
        "monocytes": input.monocytes,
        "eosinophils": input.eosinophils,
        "basophils": input.basophils,
        "platelets": input.platelets,
        "urea": input.urea,
        "creatinine": input.creatinine,
        "sodium": input.sodium,
        "potassium": input.potassium,
        "calprotectin": input.calprotectin,
        "sampling_steroids": input.sampling_steroids,
        "sampling_abx": input.sampling_abx,
        "sampling_asa": input.sampling_asa,
        "sampling_aza": input.sampling_aza,
        "sampling_mp": input.sampling_mp,
        "sampling_ifx": input.sampling_ifx,
        "sampling_ada": input.sampling_ada,
        "sampling_vedo": input.sampling_vedo,
        "sampling_uste": input.sampling_uste,
        "sampling_tofa": input.sampling_tofa,
        "sampling_mtx": input.sampling_mtx,
        "sampling_ciclosporin": input.sampling_ciclosporin,
        "sampling_filgo": input.sampling_filgo,
        "sampling_upa": input.sampling_upa,
        "sampling_risa": input.sampling_risa,
        "disease_duration_weeks": disease_duration_weeks,
        "diagnosis_year": diagnosis_year,
        "study_group_name_CD": study_group_name_CD,
        "study_group_name_IBDU": study_group_name_IBDU,
        "study_group_name_UC": study_group_name_UC,
        "montreal_cd_location_L1 Ileal": montreal_cd_location_L1_Ileal,
        "montreal_cd_location_L2 Colonic": montreal_cd_location_L2_Colonic,
        "montreal_cd_location_L3 Ileocolonic": montreal_cd_location_L3_Ileocolonic,
        "montreal_cd_behaviour_B1 Non-stricturing, non-penetrating": montreal_cd_behaviour_B1_Non_stricturing_non_penetrating,
        "montreal_cd_behaviour_B2 Stricturing": montreal_cd_behaviour_B2_Stricturing,
        "montreal_cd_behaviour_B3 Penetrating": montreal_cd_behaviour_B3_Penetrating,
        "montreal_uc_extent_E1 Proctitis": montreal_uc_extent_E1_Proctitis,
        "montreal_uc_extent_E2 Left-sided": montreal_uc_extent_E2_Left_sided,
        "montreal_uc_extent_E3 Extensive": montreal_uc_extent_E3_Extensive,
        "montreal_uc_severity_S0 Remission": montreal_uc_severity_S0_Remission,
        "montreal_uc_severity_S1 Mild": montreal_uc_severity_S1_Mild,
        "montreal_uc_severity_S2 Moderate": montreal_uc_severity_S2_Moderate,
        "montreal_uc_severity_S3 Severe": montreal_uc_severity_S3_Severe,
        "is_smoker_Ex-smoker": is_smoker_Ex_smoker,
        "is_smoker_Non-smoker": is_smoker_Non_smoker,
        "is_smoker_Smoker": is_smoker_Smoker,
        "season_autumn": season_autumn,
        "season_spring": season_spring,
        "season_summer": season_summer,
        "season_winter": season_winter,
    }

    return formatted_data_dictionary


def format_for_database(formatted_data_dictionary: dict) -> dict:
    """
    Takes formatted data dictionary and formats it for database storage.
    """
    # rename key for database storage
    formatted_data_dictionary["montreal_cd_location_L1_Ileal"] = (
        formatted_data_dictionary.pop("montreal_cd_location_L1 Ileal")
    )
    formatted_data_dictionary["montreal_cd_location_L2_Colonic"] = (
        formatted_data_dictionary.pop("montreal_cd_location_L2 Colonic")
    )
    formatted_data_dictionary["montreal_cd_location_L3_Ileocolonic"] = (
        formatted_data_dictionary.pop("montreal_cd_location_L3 Ileocolonic")
    )
    formatted_data_dictionary[
        "montreal_cd_behaviour_B1_Non_stricturing_non_penetrating"
    ] = formatted_data_dictionary.pop(
        "montreal_cd_behaviour_B1 Non-stricturing, non-penetrating"
    )
    formatted_data_dictionary["montreal_cd_behaviour_B2_Stricturing"] = (
        formatted_data_dictionary.pop("montreal_cd_behaviour_B2 Stricturing")
    )
    formatted_data_dictionary["montreal_cd_behaviour_B3_Penetrating"] = (
        formatted_data_dictionary.pop("montreal_cd_behaviour_B3 Penetrating")
    )
    formatted_data_dictionary["montreal_uc_extent_E1_Proctitis"] = (
        formatted_data_dictionary.pop("montreal_uc_extent_E1 Proctitis")
    )
    formatted_data_dictionary["montreal_uc_extent_E2_Left_sided"] = (
        formatted_data_dictionary.pop("montreal_uc_extent_E2 Left-sided")
    )
    formatted_data_dictionary["montreal_uc_extent_E3_Extensive"] = (
        formatted_data_dictionary.pop("montreal_uc_extent_E3 Extensive")
    )
    formatted_data_dictionary["montreal_uc_severity_S0_Remission"] = (
        formatted_data_dictionary.pop("montreal_uc_severity_S0 Remission")
    )
    formatted_data_dictionary["montreal_uc_severity_S1_Mild"] = (
        formatted_data_dictionary.pop("montreal_uc_severity_S1 Mild")
    )
    formatted_data_dictionary["montreal_uc_severity_S2_Moderate"] = (
        formatted_data_dictionary.pop("montreal_uc_severity_S2 Moderate")
    )
    formatted_data_dictionary["montreal_uc_severity_S3_Severe"] = (
        formatted_data_dictionary.pop("montreal_uc_severity_S3 Severe")
    )
    formatted_data_dictionary["is_smoker_Ex_smoker"] = formatted_data_dictionary.pop(
        "is_smoker_Ex-smoker"
    )
    formatted_data_dictionary["is_smoker_Non_smoker"] = formatted_data_dictionary.pop(
        "is_smoker_Non-smoker"
    )

    return formatted_data_dictionary
