from feast import FeatureStore
from app.repositories.interfaces.user_repository_interface import IUserRepository
from app.core.config import settings
from typing import Dict, Any

class UserRepository(IUserRepository):
    def __init__(self):
        # In production, this should be initialized once or managed
        self.fs = FeatureStore(repo_path=settings.FEAST_REPO_PATH)

    async def get_user_features(self, user_id: str) -> Dict[str, Any]:
        features = self.fs.get_online_features(
            features=[
                "user_risk_features:credit_score",
                "user_risk_features:income",
                "user_risk_features:total_debt",
                "user_risk_features:num_late_payments"
            ],
            entity_rows=[{"user_id": user_id}]
        ).to_dict()
        
        # Helper to extract single values from lists (Feast returns lists)
        result = {}
        for key, values in features.items():
            result[key] = values[0] if values else None
        return result

