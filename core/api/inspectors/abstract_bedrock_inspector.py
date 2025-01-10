from abc import abstractmethod
from core.api.inspectors.abstract_image_inspector import AbstractImageInspector


class AbstractBedrockInspector(AbstractImageInspector):
    @abstractmethod
    def init_inspector(self, images, policies, payload) -> None:
        print("AbstractBedrockInspector: Inspecting")
        if images is None:
            raise ValueError("Images cannot be None")
        elif policies is None:
            raise ValueError("Policies cannot be None")
        elif payload is None:
            raise ValueError("Payload cannot be None")
        else:
            super().init_inspector(images, policies, payload)
        pass
