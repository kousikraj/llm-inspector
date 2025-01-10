import json
from abc import ABC

import requests
import base64

from core.api.commons.request_payload import RequestPayload
from openai import OpenAI
from core.api.generators.abstract_image_generator import AbstractImageGenerator

key = "sk-proj-298jl9OF4cJKVvgGbmQUT3BlbkFJrKPWhdfyQ7nGue4OFVIK"


class OpenAIImageGenerator(AbstractImageGenerator, ABC):
    client = OpenAI(api_key=key)

    def init(self):
        print("OpenAIImageGenerator: Init")
        super().init()

    def build_prompt(self, payload: RequestPayload) -> None:
        print("OpenAIImageGenerator: Building Prompt")
        try:
            request_payload = payload.other_params
            request_payload.update(
                {
                    "model": payload.model_id,
                    "prompt": payload.prompt
                    + "\nI NEED to test how the tool works with extremely simple prompts. "
                    "DO NOT modify the input prompt. DO NOT add any details, effects. "
                    "Just use it AS-IS.",  # ADDING THIS TO FORCE DALL-E NOT TO IMPROVE PROMPTS
                    "size": "1024x1024",
                    "quality": "standard",
                    "n": payload.no_of_images,
                }
            )
            self.request_payload = request_payload
        except Exception as e:
            raise AttributeError(f"OpenAIImageGenerator: Invalid Payload")

    def invoke_model(self, payload: RequestPayload):
        print("OpenAIImageGenerator: Invoking Model API")

        response = self.client.images.generate(
            model=self.request_payload["model"],
            prompt=self.request_payload["prompt"],
            size=self.request_payload["size"],
            quality=self.request_payload["quality"],
            n=self.request_payload["n"],
        )
        # Get response and log it for audit
        self.generator_response = json.loads(response.to_json())

    def save_image_in_temp(self, image_base64_str) -> None:
        print("OpenAIImageGenerator: Saving Image in Temp")
        image_url = self.generator_response["data"][0]["url"]
        image_response = requests.get(image_url)
        image_base64_str = base64.b64encode(image_response.content).decode("utf-8")
        super().save_image_in_temp(image_base64_str)

    def save_images_and_prompt(self, response_without_image) -> None:
        if response_without_image is None:
            response_without_image = self.generator_response.copy()
        super().save_images_and_prompt(response_without_image)

    def inspect_response(self, policies) -> None:
        print("OpenAIImageGenerator: Validating Response")
        super().inspect_response(policies)
