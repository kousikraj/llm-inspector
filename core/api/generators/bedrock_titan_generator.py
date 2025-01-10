from abc import ABC
import base64
from core.api.generators.abstract_bedrock_generator import AbstractBedrockImageGenerator
from core.api.commons.request_payload import RequestPayload


class BedrockTitanImageGenerator(AbstractBedrockImageGenerator, ABC):
    def init(self):
        print("BedrockTitanImageGenerator: Init")
        super().init()

    def build_prompt(self, payload: RequestPayload) -> None:
        print("BedrockTitanImageGenerator: Building Request")
        try:
            request_payload = payload.other_params
            if "imageGenerationConfig" in payload.other_params:
                request_payload["imageGenerationConfig"].update(
                    {
                        "numberOfImages": payload.no_of_images,  # Range: 1 to 5
                        "seed": payload.seed,  # Range: 0 to 214783647
                    }
                )
            request_payload.update(
                {
                    "taskType": payload.type.value,
                    "textToImageParams": {
                        "text": payload.prompt,  # Required
                        "negativeText": ", ".join(payload.negative_prompts),
                    },
                }
            )
            self.request_payload = request_payload
        except Exception as e:
            raise AttributeError("Invalid Payload")

    def invoke_model(self, payload):
        print("TitanImageGenerator: Invoking Model API")
        response = super().invoke_model(payload={"body": self.request_payload})
        self.generator_response = response

    def save_image_in_temp(self, image_b64_str) -> None:
        print("TitanImageGenerator: Saving Image in Temp")
        for image_b64_str in self.generator_response["images"]:
            super().save_image_in_temp(image_b64_str)

    def save_images_and_prompt(self, response_without_image) -> None:
        if response_without_image is None:
            response_without_image = self.generator_response.copy()
        del response_without_image["images"]
        super().save_images_and_prompt(response_without_image)

    def inspect_response(self, policies) -> None:
        print("TitanImageGenerator: Inspect Response")
        super().inspect_response(policies)
