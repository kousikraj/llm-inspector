from abc import ABC, abstractmethod
import base64
import io
import os
from PIL import Image
import uuid

from core.api.commons import constants
from core.api.commons.request_payload import RequestPayload
from core.api.commons.utility import save_images_and_payload

os.makedirs(constants.LOCAL_TEMP_FOLDER_PATH, exist_ok=True)


def decode_and_save_locally(img_b64, file_name):
    """Decodes image and saves locally"""
    img = Image.open(io.BytesIO(base64.decodebytes(bytes(img_b64, "utf-8"))))
    img.save(file_name)
    return img


class AbstractImageGenerator(ABC):
    """
    The Abstract Image Generator defines a template method that contains a skeleton of
    model details, payload and other pre-processing operations.
    """

    def __init__(self):
        self.inspectors = None
        self.req_id = None
        self.request_payload_object: RequestPayload = None
        self.request_payload = None
        self.generator_response = None
        self.generated_images = []
        self.inspector_response = None

    @abstractmethod
    def init(self):
        self.req_id = str(uuid.uuid4())
        pass

    def generate(self, payload: RequestPayload, inspectors, policies) -> None:
        """
        This function calls all sequence of operations to validate request before executing the API
        """
        self.init()
        self.request_payload_object = payload
        self.request_payload_object.req_id = self.req_id
        self.build_prompt(payload)
        self.invoke_model(payload)
        self.save_model_response()
        self.save_image_in_temp(None)
        self.save_images_and_prompt(None)
        self.inspectors = inspectors
        self.inspect_response(policies)

    @abstractmethod
    def build_prompt(self, payload: RequestPayload) -> None:
        pass

    @abstractmethod
    def save_images_and_prompt(self, response_without_image) -> None:
        print("AbstractImageGenerator: Saving Prompt to DDB")
        save_images_and_payload(
            response_without_image, self.generated_images, self.request_payload_object
        )

    @abstractmethod
    def invoke_model(self, payload):
        pass

    def save_model_response(self) -> None:
        pass

    @abstractmethod
    def save_image_in_temp(self, image_b64_str) -> None:
        print("AbstractImageGenerator: Saving Image")
        if image_b64_str is None:
            raise ValueError("Invalid parameters. Image cannot be None")
        file_name = f"" + str(uuid.uuid4()) + ".png"
        # Decode and save image locally
        local_file_name = constants.LOCAL_TEMP_FOLDER_PATH + file_name
        img_for_display = decode_and_save_locally(image_b64_str, local_file_name)
        self.generated_images.append(local_file_name)
        # @Todo Delete this line during deployment
        img_for_display.show()
        print("AbstractImageGenerator: Saved Image : " + file_name)
        return None

    @abstractmethod
    def inspect_response(self, policies) -> None:
        print("AbstractImageGenerator: Inspect Response")
        if (
            self.inspectors is not None
            and policies is not None
            and self.request_payload is not None
        ):
            for inspector in self.inspectors:
                inspector.init_inspector(
                    self.generated_images, policies, self.request_payload_object
                )
        else:
            raise ValueError(
                "Invalid parameters. Inspectors, Policies and Payload cannot be None"
            )
