import httpx

class AIClient:
    async def moderate_text(self, text: str):
        # Mock OpenAI API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/moderations",
                json={"input": text},
                headers={"Authorization": "Bearer <API_KEY>"},
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception("AI service unavailable")