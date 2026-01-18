from abc import ABC, abstractmethod
from app.schemas.user import PredictionResponse

class IUserService(ABC):
    @abstractmethod
    async def predict_risk(self, user_id: str) -> PredictionResponse:
        pass

