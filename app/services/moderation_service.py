from app.utils.ai_client import AIClient
from app.services.cache_service import CacheService
from app.db.repositories import ModerationRepository

class ModerationService:
    def __init__(self):
        self.ai_client = AIClient()
        self.cache_service = CacheService()
        self.repository = ModerationRepository()

    async def moderate_text(self, text: str):
        # Check cache first
        cached_result = self.cache_service.get(text)
        if cached_result:
            return cached_result

        # Call OpenAI API (or mock)
        result = await self.ai_client.moderate_text(text)

        # Cache the result
        self.cache_service.set(text, result)

        # Save to database
        self.repository.save_result(text, result)

        return result