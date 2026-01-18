from pydantic import BaseModel

class PredictionRequest(BaseModel):
    user_id: str

class PredictionResponse(BaseModel):
    user_id: str
    risk_score: float
    risk_level: str

