import datetime
from typing import Literal

from pydantic import BaseModel
from pydantic.fields import Field


class Input(BaseModel):
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
