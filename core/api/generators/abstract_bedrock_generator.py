from abc import abstractmethod
from core.api.generators.abstract_image_generator import AbstractImageGenerator

import json
import boto3

boto3_bedrock = boto3.client("bedrock-runtime")


class AbstractBedrockImageGenerator(AbstractImageGenerator):
    """
    Abstract base class for generating images using the Amazon Bedrock service.

    This class defines the common interface and behavior for invoking Amazon Bedrock
    models through an API. Concrete subclasses should implement the `invoke_model`
    method with their specific logic for interacting with the Bedrock service.

    Inherits from:
        AbstractImageGenerator: An abstract base class for generating images.
    """

    @abstractmethod
    def invoke_model(self, payload):
        """
        Invoke the Amazon Bedrock model through the API.

        This method calls the respective Amazon Bedrock model through the API
        and returns the response body as a Python object.

        Args:
            payload (dict): A dictionary containing the necessary data for invoking
                the Bedrock model, including the request body and model ID.

        Returns:
            dict: The response body from the Bedrock model API as a Python dictionary.

        Raises:
            ValueError: If the `payload` or its required keys ("body", "model_id")
                are `None` or missing.
        """
        print("BedrockImageGenerator: Invoking Model API")
        """Calls respective Bedrock Model through API. Returns body from Reponse"""
        if payload is None:
            raise ValueError("Policies and Payload cannot be None")
        else:
            if "body" in payload:
                response = boto3_bedrock.invoke_model(
                    body=json.dumps(self.request_payload),
                    modelId=self.request_payload_object.model_id,
                    accept="application/json",
                    contentType="application/json",
                )
                return json.loads(response.get("body").read())
            else:
                raise ValueError("Payload should have both 'body' and 'model_id'")
        pass
