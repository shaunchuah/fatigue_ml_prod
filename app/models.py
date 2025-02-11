import datetime
from typing import Literal, Optional

from pydantic import BaseModel
from pydantic.fields import Field
from sqlmodel import Field, SQLModel


class Input(BaseModel):
    cucq_5: int = Field(ge=0, le=14)
    has_active_symptoms: int = Field(
        ge=0, le=1, description="Has symptoms of active IBD, 0 or 1"
    )
    age: int = Field(ge=0, le=200, description="Current age")
    sex: int = Field(ge=0, le=1, description="1 is male, 0 is female")
    height: float = Field(ge=0, le=300, description="Height in cm")
    weight: float = Field(ge=0, le=300, description="Weight in kg")
    age_at_diagnosis: int = Field(ge=0, le=200, description="Age at diagnosis")
    montreal_upper_gi: int = Field(ge=0, le=1)
    montreal_perianal: int = Field(ge=0, le=1)
    albumin: float = Field(ge=0, le=100)
    crp: float = Field(ge=0, le=500)
    haemoglobin: float = Field(ge=0, le=300)
    red_cell_count: float
    white_cell_count: float
    neutrophils: float
    lymphocytes: float
    monocytes: float
    eosinophils: float
    basophils: float
    platelets: float = Field(ge=0, le=1500)
    urea: float = Field(ge=0, le=30)
    creatinine: float = Field(ge=0, le=1000)
    sodium: float = Field(ge=110, le=160)
    potassium: float = Field(ge=0, le=10)
    calprotectin: float = Field(ge=0, le=2000)
    sampling_steroids: int = Field(ge=0, le=1)
    sampling_abx: int = Field(ge=0, le=1)
    sampling_asa: int = Field(ge=0, le=1)
    sampling_aza: int = Field(ge=0, le=1)
    sampling_mp: int = Field(ge=0, le=1)
    sampling_ifx: int = Field(ge=0, le=1)
    sampling_ada: int = Field(ge=0, le=1)
    sampling_vedo: int = Field(ge=0, le=1)
    sampling_uste: int = Field(ge=0, le=1)
    sampling_tofa: int = Field(ge=0, le=1)
    sampling_mtx: int = Field(ge=0, le=1)
    sampling_ciclosporin: int = Field(ge=0, le=1)
    sampling_filgo: int = Field(ge=0, le=1)
    sampling_upa: int = Field(ge=0, le=1)
    sampling_risa: int = Field(ge=0, le=1)
    date_of_diagnosis: datetime.date
    study_group: Literal["cd", "ibdu", "uc"]
    montreal_cd_location: Literal["l1", "l2", "l3", "0"]
    montreal_cd_behaviour: Literal["b1", "b2", "b3", "0"]
    montreal_uc_extent: Literal["e1", "e2", "e3", "0"]
    montreal_uc_severity: Literal["s0", "s1", "s2", "s3", "0"]
    is_smoker: Literal["Ex-smoker", "Non-smoker", "Smoker"]


class InputData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    has_active_symptoms: int
    age: int
    sex: int
    height: float
    weight: float
    bmi: float
    age_at_diagnosis: int
    montreal_upper_gi: int
    montreal_perianal: int
    albumin: float
    crp: float
    haemoglobin: float
    red_cell_count: float
    white_cell_count: float
    neutrophils: float
    lymphocytes: float
    monocytes: float
    eosinophils: float
    basophils: float
    platelets: float
    urea: float
    creatinine: float
    sodium: float
    potassium: float
    calprotectin: float
    sampling_steroids: int
    sampling_abx: int
    sampling_asa: int
    sampling_aza: int
    sampling_mp: int
    sampling_ifx: int
    sampling_ada: int
    sampling_vedo: int
    sampling_uste: int
    sampling_tofa: int
    sampling_mtx: int
    sampling_ciclosporin: int
    sampling_filgo: int
    sampling_upa: int
    sampling_risa: int
    disease_duration_weeks: float
    diagnosis_year: int
    study_group_name_CD: int
    study_group_name_IBDU: int
    study_group_name_UC: int
    montreal_cd_location_L1_Ileal: int
    montreal_cd_location_L2_Colonic: int
    montreal_cd_location_L3_Ileocolonic: int
    montreal_cd_behaviour_B1_Non_stricturing_non_penetrating: int
    montreal_cd_behaviour_B2_Stricturing: int
    montreal_cd_behaviour_B3_Penetrating: int
    montreal_uc_extent_E1_Proctitis: int
    montreal_uc_extent_E2_Left_sided: int
    montreal_uc_extent_E3_Extensive: int
    montreal_uc_severity_S0_Remission: int
    montreal_uc_severity_S1_Mild: int
    montreal_uc_severity_S2_Moderate: int
    montreal_uc_severity_S3_Severe: int
    is_smoker_Ex_smoker: int
    is_smoker_Non_smoker: int
    is_smoker_Smoker: int
    season_autumn: int
    season_spring: int
    season_summer: int
    season_winter: int
    predicted_probability: float
    predicted_class: str
    correct_class: str
    cucq_5: int
    correct_prediction: bool
    created_at: datetime.datetime = Field(
        default=datetime.datetime.now(datetime.timezone.utc)
    )
