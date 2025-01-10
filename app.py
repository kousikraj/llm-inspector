#!/usr/bin/env python3
import aws_cdk as cdk
from constructs import Construct
from stack.cdk.llm_inspector_stack import LlmInspectorStack

app = cdk.App()
LlmInspectorStack(app, "llm-inspector")
app.synth()

# json_object = json.dumps(
#     {
#         "s3_bucket_name": llm_stack.s3_name.value,
#         "ddb_name": llm_stack.table_name.value,
#     },
#     indent=4,
# )
#
# if not os.path.exists("core/api/env"):
#     os.makedirs("core/api/env")
#
# with open("core/api/env/stack.json", "w") as outfile:
#     outfile.write(json_object)
