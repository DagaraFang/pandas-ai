from typing import Optional, Union
import requests
from pandasai.extensions.llms.litellm.pandasai_litellm.litellm import LiteLLM


class DeepSeekLLM(LiteLLM):
    """
    A class to represent a DeepSeek LLM.
    """

    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        """
        Initialize the DeepSeek LLM.

        Args:
            api_key (str): The API key for DeepSeek.
            model (str): The model name for DeepSeek. Defaults to "deepseek-chat".
        """
        super().__init__(model=model, api_key=api_key)

    def _get_endpoint(self):
        """
        Get the endpoint for DeepSeek API.

        Returns:
            str: The endpoint URL.
        """
        return "https://api.deepseek.com/chat/completions"

    def _get_headers(self):
        """
        Get the headers for the DeepSeek API request.

        Returns:
            dict: The headers.
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _make_request(self, prompt: str):
        """
        Make a request to the DeepSeek API.

        Args:
            prompt (str): The prompt to send to the API.

        Returns:
            dict: The response from the API.
        """
        headers = self._get_headers()
        endpoint = self._get_endpoint()
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def generate_code(self, prompt: str) -> str:
        """
        Generate code using the DeepSeek LLM.

        Args:
            prompt (str): The prompt to send to the LLM.

        Returns:
            str: The generated code.
        """
        response = self._make_request(prompt)
        return response["choices"][0]["message"]["content"]