from dataclasses import dataclass, field
from enum import Enum
from core.api.commons.model_type import ModelType


@dataclass
class RequestPayload:
    """
    Request payload for constructing payload to call LLMs
    """

    class TaskType(Enum):
        """
        Enum for task type
        """

        TEXT = "text"
        IMAGE = "image"
        TEXT_IMAGE = "TEXT_IMAGE"

    model_id: ModelType
    prompt: str
    type: TaskType

    seed: int
    no_of_images: int

    req_id: str = field(default=None)
    temperature: float = field(default=None)
    other_params: {} = field(default=None)
    top_p: float = field(default=None)
    max_tokens: int = field(default=None)
    negative_prompts: [] = field(default=list)

    def toJSON(self):
        return {
            "model_id": self.model_id,
            "prompt": self.prompt,
            "type": self.type.value,
            "seed": self.seed,
            "no_of_images": self.no_of_images,
            "req_id": self.req_id,
            "temperature": self.temperature,
            "other_params": self.other_params,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens,
            "negative_prompts": self.negative_prompts,
        }
