import os
from typing import Any

from openai import OpenAI
from utils.api_key_manager import APIKeyManager


class Model:
    def __init__(self, model_name, base_url, api_keys_file, context):
        self.model_name = model_name
        self.base_url = base_url
        self.context = context
        self.api_key_manager = APIKeyManager()
        self.client = None
        self.update_client()
        
    def update_client(self) -> None:
        api_key = self.api_key_manager.get_next_available_key()
        if not api_key:
            raise Exception("No available API keys")
            
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=api_key,
            default_headers={
                "api-key": api_key,
                "Content-Type": "application/json"
            }
        )

    def get_instructions_for_objective(self, *args) -> dict[str, Any]:
        pass

    def format_user_request_for_llm(self, *args):
        pass

    def convert_llm_response_to_json_instructions(self, *args) -> dict[str, Any]:
        pass

    def cleanup(self, *args):
        pass
