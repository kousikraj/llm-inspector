from abc import ABC, abstractmethod

from core.api.commons.utility import update_to_ddb


class AbstractImageInspector(ABC):
    """
    The Abstract Image Inspector defines a template method that contains a skeleton of
    model details to inspect, payload and other pre-processing operations.
    """

    def __init__(self):
        self.images = None
        self.policies = None
        self.payload = None

    @abstractmethod
    def init_inspector(self, images, policies, payload) -> None:
        """
        This function calls all sequence of operations to validate request before executing the API
        """
        print("AbstractImageInspector: Inspecting")
        self.images = images
        self.policies = policies
        self.payload = payload
        self.inspect()

    @abstractmethod
    def inspect(self) -> None:
        print("AbstractImageInspector: Inspecting")

    @abstractmethod
    def save_inspected_results(self, image, response_body) -> None:
        print("AbstractImageInspector: Saving Inspected Results")
        update_to_ddb(self.payload.model_id, self.payload.req_id, image, response_body)
