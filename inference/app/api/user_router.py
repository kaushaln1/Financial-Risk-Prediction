from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import PredictionRequest, PredictionResponse
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.services.interfaces.user_service_interface import IUserService

router = APIRouter()

# Dependency Injection
def get_user_service() -> IUserService:
    repo = UserRepository()
    return UserService(repo)

@router.post("/predict", response_model=PredictionResponse)
async def predict_risk(
    request: PredictionRequest, 
    service: IUserService = Depends(get_user_service)
):
    try:
        return await service.predict_risk(request.user_id)
    except Exception as e:
        # In production, log error and return generic message
        raise HTTPException(status_code=500, detail=str(e))
