import aws_cdk as core
import aws_cdk.assertions as assertions

from stack.cdk.llm_inspector_stack import LlmInspectorStack


# example tests. To run these tests, uncomment this file along with the example
# resource in llm_inspector/llm_inspector_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = LlmInspectorStack(app, "llm-inspector")
    template = assertions.Template.from_stack(stack)


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
