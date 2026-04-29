import httpx
from typing import Dict, Union

from app.core.config import settings
from app.services.decorator import handle_service_errors

class OpenRouterClient:
    def __init__(self):
        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": settings.OPENROUTER_SITE_URL,
            "X-Title": settings.OPENROUTER_APP_NAME
        }
        self.headers = headers
        self._client: httpx.AsyncClient | None = None
        

    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            base_url=settings.OPENROUTER_BASE_URL,
            headers=self.headers,
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()
    
    @handle_service_errors
    async def post_chat(self, req: Dict[str, Union[str, float, list]]) -> str:
        if self._client is None:
            raise RuntimeError("OpenRouterClient must be used as async context manager")
        
        response = await self._client.post(
            '/chat/completions',
            json=req
        )
        response.raise_for_status()

        response_json = response.json()
        
        return self._extract_content_from_response(response_json)

    def _extract_content_from_response(self, data: Dict[str, Union[str, float, list]]) -> str:
        choices = data.get('choices', [])
        if not choices:
            raise Exception("empty choices in openrouter respone")
        
        first_choice = choices[0]

        if 'message' in first_choice:
            message = first_choice['message']
            if 'content' in message:
                content = message['content']
                if content:
                    return content
                else:
                    raise Exception("empty content in openrouter respone")
                
        raise Exception("empty response in openrouter respone")