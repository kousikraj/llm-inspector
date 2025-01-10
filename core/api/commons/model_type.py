from enum import Enum


class ModelType(Enum):
    OPEN_AI_DALLE = "dall-e-3"
    BEDROCK_TITAN_IMAGE = "amazon.titan-image-generator-v1"
    BEDROCK_SDXL = "stability.stable-diffusion-xl-v1"
    BEDROCK_ANTHROPHIC_CLAUDE_SONNET = "anthropic.claude-3-sonnet-20240229-v1:0"
    BEDROCK_ANTHROPHIC_VERSION = "bedrock-2023-05-31"
