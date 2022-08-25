from pydantic import BaseModel


class MedicalRecord(BaseModel):
    id: str
    state: str
    healthcare_unit: str
    issue_date: int
    performed_procedure: str
    hashed_patient_identifier: str
    age: int
    gender: str
    race: int
    nationality: str
    reason_for_encounter: str
    reason_for_discharge: int
    date_of_discharge: int
    associated_causes: str
    main_diagnosis: str
    secondary_diagnosis: str
    ethnic_group: str
    weight: int
    height: int
    indicator_of_transplantation: str
    number_of_transplantation: int

class Prediction(BaseModel):
    cluster: int
