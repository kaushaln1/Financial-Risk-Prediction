import mlflow
import mlflow.sklearn
import pandas as pd
from app.services.interfaces.user_service_interface import IUserService
from app.repositories.interfaces.user_repository_interface import IUserRepository
from app.schemas.user import PredictionResponse
from app.core.config import settings

class UserService(IUserService):
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo
        mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
        
        try:
            print(f"Loading model {settings.MODEL_NAME} stage {settings.MODEL_STAGE}...")
            # Try to load model directly via run ID if available, or just catch the registry error
            # But the real issue is 'models:/' uses the tracking server which is rejecting us.
            # We can try to use the artifact location directly if we had it.
            # However, let's fix the call first. 
            self.model = mlflow.sklearn.load_model(
                model_uri=f"models:/{settings.MODEL_NAME}/{settings.MODEL_STAGE}"
            )
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Warning: Could not load model: {e}. Inference will fail.")
            # Fallback: Try to load from the latest run in the experiment if registry fails
            try:
                print("Attempting fallback: Loading latest model from experiment...")
                current_experiment = mlflow.get_experiment_by_name("financial_risk_prediction")
                if current_experiment:
                    runs = mlflow.search_runs(
                        experiment_ids=[current_experiment.experiment_id],
                        order_by=["start_time DESC"],
                        max_results=1
                    )
                    if not runs.empty:
                        last_run_id = runs.iloc[0].run_id
                        print(f"Loading from run_id: {last_run_id}")
                        self.model = mlflow.sklearn.load_model(f"runs:/{last_run_id}/model")
                        print("Fallback load successful.")
                    else:
                        self.model = None
                else:
                    self.model = None
            except Exception as e2:
                print(f"Fallback failed: {e2}")
                self.model = None

    async def predict_risk(self, user_id: str) -> PredictionResponse:
        features = await self.user_repo.get_user_features(user_id)
        
        if not self.model:
            raise RuntimeError("Model is not loaded.")

        # Prepare for model
        input_data = pd.DataFrame([features])
        
        # Ensure column order matches training
        required_cols = ["credit_score", "income", "total_debt", "num_late_payments"]
        
        # Simple validation
        if not all(col in input_data.columns for col in required_cols):
             # Fallback or error if features missing
             raise ValueError(f"Missing features. Got {input_data.columns}")

        input_data = input_data[required_cols]

        prediction = self.model.predict(input_data)[0]
        
        if hasattr(self.model, "predict_proba"):
            risk_score = self.model.predict_proba(input_data)[0][1] # Probability of class 1
        else:
            risk_score = float(prediction)

        return PredictionResponse(
            user_id=user_id,
            risk_score=float(risk_score),
            risk_level="HIGH" if risk_score > 0.5 else "LOW"
        )

