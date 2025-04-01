import asyncio
import aiohttp
import json
import logging
import certifi
import ssl
import requests
from config.logger import logger

ssl_context = ssl.create_default_context(cafile=certifi.where())

class PerplexityClient:
    def __init__(self, api_key: str, api_url: str, model: str):
        self.api_key = api_key
        self.api_url = api_url
        self.model = model

    def get_response_sync(self, messages:list, response_format: dict=None, timeout: int = 120) -> str:
        """
            Synchronous function to get a response from the Perplexity API.
            Uses the requests library for blocking API calls.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "response_format": response_format
        }
        
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Request payload: %s", json.dumps(payload, indent=2))
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=timeout)
            response.raise_for_status()
            json_response = response.json()
            return json_response["choices"][0]["message"]["content"]
        except requests.Timeout:
            logger.error(f"⏳ API request timed out after %d seconds{timeout}" )
            return None
        except Exception as e:
            logger.error(f"❌ API request failed: {e}")
            return None

    async def get_response(self, messages:list, response_format: dict=None, timeout: int = 120) -> str:
        """
        Async function to get response from Perplexity API.
        Uses aiohttp for non-blocking API calls.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "response_format": response_format
        }
        
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Request payload: %s", json.dumps(payload, indent=2))
     
        try:
            async with aiohttp.request("POST", self.api_url, ssl=ssl_context, headers=headers, json=payload, timeout=aiohttp.ClientTimeout(timeout)) as response:
                response.raise_for_status()
                json_response = await response.json()
                return json_response["choices"][0]["message"]["content"]
            
        except asyncio.TimeoutError:
            logger.error("⏳ API request timed out after %d seconds {timeout}")
            return None
        except Exception as e:
            logger.error(f"❌ API request failed: {e}")
            return None
