from abc import ABC, abstractmethod
from typing import Dict, Any

class IUserRepository(ABC):
    @abstractmethod
    async def get_user_features(self, user_id: str) -> Dict[str, Any]:
        pass

