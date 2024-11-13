import json
import time
from typing import Any

from models.model import Model
from openai.types.beta.threads.message import Message
from utils.screen import Screen


# TODO
# [ ] Function calling with assistants api - https://platform.openai.com/docs/assistants/tools/function-calling/quickstart

class GPT4o(Model):
    def __init__(self, model_name, base_url, api_key, context):
        super().__init__(model_name, base_url, api_key, context)

    def get_instructions_for_objective(self, original_user_request: str, step_num: int = 0) -> dict[str, Any]:
        message = self.format_user_request_for_llm(original_user_request, step_num)
        response = self.send_message_to_llm(message)
        return self.convert_llm_response_to_json_instructions(response)

    def format_user_request_for_llm(self, original_user_request, step_num) -> list[dict[str, Any]]:
        base64_img: str = Screen().get_screenshot_in_base64()

        request_data: str = json.dumps({
            'original_user_request': original_user_request,
            'step_num': step_num
        })

        message = [
            {
                'role': 'system',
                'content': self.context
            },
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'text',
                        'text': request_data
                    },
                    {
                        'type': 'image_url',
                        'image_url': {
                            'url': f'data:image/jpeg;base64,{base64_img}'
                        }
                    }
                ]
            }
        ]
        return message

    def send_message_to_llm(self, messages) -> Any:
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            return response
        except Exception as e:
            print(f"Error in send_message_to_llm: {str(e)}")
            raise

    def convert_llm_response_to_json_instructions(self, llm_response) -> dict[str, Any]:
        try:
            response_text = llm_response.choices[0].message.content.strip()
            # Find JSON content
            start_index = response_text.find('{')
            end_index = response_text.rfind('}')
            
            if start_index != -1 and end_index != -1:
                json_str = response_text[start_index:end_index + 1]
                return json.loads(json_str)
            return {}
        except Exception as e:
            print(f"Error parsing response: {str(e)}")
            return {}

    def cleanup(self):
        # Note: Cannot delete screenshots while the thread is active. Cleanup during shut down.
        for id in self.list_of_image_ids:
            self.client.files.delete(id)
        self.thread = self.client.beta.threads.create()  # Using old thread even by accident would cause Image errors
