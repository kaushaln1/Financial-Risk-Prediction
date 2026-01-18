from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Financial Risk Prediction API"
    # Default to where we mount the feature store in Docker/K8s
    FEAST_REPO_PATH: str = "./features" 
    MLFLOW_TRACKING_URI: str = "http://mlflow-service:5000"
    MODEL_NAME: str = "financial_risk_model"
    MODEL_STAGE: str = "Staging"

    class Config:
        env_file = ".env"

settings = Settings()

