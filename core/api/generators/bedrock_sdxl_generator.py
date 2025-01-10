from abc import ABC

from core.api.generators.abstract_bedrock_generator import AbstractBedrockImageGenerator
from core.api.commons.request_payload import RequestPayload


class SDXLImageGenerator(AbstractBedrockImageGenerator, ABC):
    def init(self):
        print("SDXLImageGenerator: Init")
        super().init()

    def build_prompt(self, payload: RequestPayload) -> None:
        print("SDXLImageGenerator: Validating Request")
        try:
            request_payload = payload.other_params
            request_payload.update(
                {
                    "text_prompts": [{"text": payload.prompt, "weight": 1.0}]
                    + [
                        {"text": negprompt, "weight": -1.0}
                        for negprompt in payload.negative_prompts
                    ],
                    "seed": payload.seed,
                }
            )
            self.request_payload = request_payload
        except Exception as e:
            print(e)
            raise AttributeError("Invalid Payload")

    def invoke_model(self, payload):
        # Authentication
        print("SDXLImageGenerator: Invoking Model API")
        model_id = "stability.stable-diffusion-xl-v1"
        response = super().invoke_model(payload={"body": payload, "model_id": model_id})
        self.generator_response = response

    def save_image_in_temp(self, image_b64_str) -> None:
        print("SDXLImageGenerator: Saving Image in Temp")
        artifacts = self.generator_response["artifacts"]
        for image_b64 in artifacts:
            image_b64_str = image_b64.get("base64")
            super().save_image_in_temp(image_b64_str)

    def save_images_and_prompt(self, response_without_image) -> None:
        if response_without_image is None:
            response_without_image = self.generator_response.copy()
        del response_without_image["artifacts"]
        super().save_images_and_prompt(response_without_image)

    def inspect_response(self, policies) -> None:
        print("SDXLImageGenerator: Validating Response")
        super().inspect_response(policies)
