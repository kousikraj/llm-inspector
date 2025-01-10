from aws_cdk import Stack, aws_dynamodb as _ddb, aws_s3 as _s3
import os
import typing
from core.api.commons import constants
import aws_cdk
from aws_cdk import (
    aws_s3 as s3,
    Stack,
    aws_s3_deployment as s3_deployment,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as cloudfront_origins,
    aws_cognito as cognito,
    aws_apigatewayv2_authorizers_alpha as gtwy_auth,
    aws_apigateway as api_gtwy,
    aws_cognito_identitypool_alpha as id_pool,
    CfnOutput,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_dynamodb as dynamodb,
    Duration,
    aws_logs as logs,
)
from aws_cdk.aws_cognito_identitypool_alpha import (
    IdentityPoolAuthenticationProviders,
    UserPoolAuthenticationProvider,
)
from constructs import Construct


class LlmInspectorStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        aws_cdk.Tags.of(scope).add("App", "LLMInspectorStack")

        llm_inspector_s3_bucket = _s3.Bucket(
            self,
            id="llm-inspector-001",
            encryption=_s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
        )

        llm_inspector_ddb = _ddb.Table(
            self,
            "llm-inspector-ddb-001",
            partition_key=_ddb.Attribute(
                name="mId",
                type=_ddb.AttributeType.STRING,
            ),
            sort_key=_ddb.Attribute(
                name="rId",
                type=_ddb.AttributeType.STRING,
            ),
            billing_mode=_ddb.BillingMode.PAY_PER_REQUEST,
        )

        self.s3_name = aws_cdk.CfnOutput(
            self,
            "llm_inspector_s3_bucket",
            value=llm_inspector_s3_bucket.bucket_name,
            export_name="llm-inspector-s3-bucket",
        )

        self.table_name = aws_cdk.CfnOutput(
            self,
            "llm_inspector_ddb",
            value=llm_inspector_ddb.table_name,
            export_name="llm-inspector-ddb-name",
        )

        lambda_runtime = typing.cast(_lambda.Runtime, _lambda.Runtime.PYTHON_3_11)

        webapp_bucket = s3.Bucket(
            self, id="llm_inspector_web", access_control=s3.BucketAccessControl.PRIVATE
        )

        origin_access_identity = cloudfront.OriginAccessIdentity(
            self, "llm_inspector_oai"
        )
        llm_inspector_s3_bucket.grant_read(origin_access_identity)

        distribution = cloudfront.Distribution(
            self,
            "llm_inspector_cdn",
            default_root_object="index.html",
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=404, response_page_path="/index.html"
                )
            ],
            default_behavior=cloudfront.BehaviorOptions(
                origin=cloudfront_origins.S3Origin(
                    webapp_bucket, origin_access_identity=origin_access_identity
                ),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.HTTPS_ONLY,
            ),
        )

        web_deployment = s3_deployment.BucketDeployment(
            self,
            "llm_inspector_app_deployment",
            sources=[
                s3_deployment.Source.asset(os.path.join("./stack/web_app/build")),
            ],
            distribution=distribution,
            destination_bucket=webapp_bucket,
        )

        lambda_role = iam.Role(
            self,
            "llm_ins_app_role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "SecretsManagerReadWrite"
                ),
            ],
        )

        proxy_func = _lambda.Function(
            self,
            "proxy_fn",
            runtime=lambda_runtime,
            handler="proxy.handler",
            code=_lambda.Code.from_asset("stack/lambdas"),
            role=lambda_role,
        )

        user_pool = cognito.UserPool(
            self,
            "user_pool",
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(email=True),
        )

        cognito_app_client = cognito.UserPoolClient(
            self, "user_pool_client_id", user_pool=user_pool, generate_secret=False
        )

        user_pool_auth_provider = UserPoolAuthenticationProvider(
            user_pool=user_pool, user_pool_client=cognito_app_client
        )
        identity_pool_auth_providers = IdentityPoolAuthenticationProviders(
            user_pools=[user_pool_auth_provider]
        )

        cognito_idp = id_pool.IdentityPool(
            self,
            "identity_provider",
            allow_unauthenticated_identities=False,
            authentication_providers=identity_pool_auth_providers,
        )

        cognito_http_authorizer = gtwy_auth.HttpUserPoolAuthorizer(
            "http_authorizer", user_pool, user_pool_clients=[cognito_app_client]
        )

        api_log_group = logs.LogGroup(self, "llm_ins_api_logs")
        api_log_group.grant_write(cognito_idp.authenticated_role)

        rest_api = api_gtwy.RestApi(
            self,
            "llm_rest_api",
            cloud_watch_role=True,
            deploy_options=api_gtwy.StageOptions(
                stage_name="dev",
                access_log_destination=api_gtwy.LogGroupLogDestination(
                    log_group=api_log_group
                ),
                access_log_format=api_gtwy.AccessLogFormat.json_with_standard_fields(
                    caller=True,
                    http_method=True,
                    ip=True,
                    protocol=True,
                    request_time=True,
                    resource_path=True,
                    response_length=True,
                    status=True,
                    user=True,
                ),
            ),
            default_cors_preflight_options=api_gtwy.CorsOptions(
                allow_headers=[
                    "Content-Type",
                    "X-Amz-Date",
                    "Authorization",
                    "X-Api-Key",
                    "x-amz-security-token",
                ],
                allow_methods=["OPTIONS", "GET", "POST", "PUT", "PATCH", "DELETE"],
                allow_origins=["*"],
                allow_credentials=True,
                max_age=Duration.seconds(300),
            ),
        )

        client_metric = rest_api.metric_count()

        list_fn = _lambda.Function(
            self,
            "list_api_fn",
            runtime=lambda_runtime,
            handler="list.handler",
            code=_lambda.Code.from_asset("stack/lambdas"),
            role=lambda_role,
            environment={"llm_ddb": llm_inspector_ddb.table_name},
        )
        list_fn.grant_invoke(cognito_idp.authenticated_role)
        llm_inspector_ddb.grant_full_access(cognito_idp.authenticated_role)
        llm_inspector_ddb.grant_read_write_data(list_fn.role)
        llm_inspector_ddb.grant_read_write_data(cognito_idp.authenticated_role)

        list_api = rest_api.root.add_resource("list")
        list_fn_integration = api_gtwy.LambdaIntegration(
            credentials_passthrough=True,
            handler=list_fn,
        )
        list_api.add_method(
            http_method="ANY",
            authorization_type=api_gtwy.AuthorizationType(
                api_gtwy.AuthorizationType.IAM
            ),
            integration=list_fn_integration,
        ).grant_execute(cognito_idp.authenticated_role)

        details_fn = _lambda.Function(
            self,
            "details_api_fn",
            runtime=lambda_runtime,
            handler="details.handler",
            code=_lambda.Code.from_asset("stack/lambdas"),
            role=lambda_role,
            environment={
                "llm_ddb": llm_inspector_ddb.table_name,
                "llm_s3": llm_inspector_s3_bucket.bucket_name,
            },
        )
        details_fn.grant_invoke(cognito_idp.authenticated_role)
        llm_inspector_ddb.grant_read_write_data(details_fn.role)
        llm_inspector_s3_bucket.grant_read(details_fn.role)

        details_api = rest_api.root.add_resource("details")
        details_with_id = details_api.add_resource("{key}")
        details_fn_integration = api_gtwy.LambdaIntegration(
            credentials_passthrough=True,
            handler=details_fn,
        )
        details_with_id.add_method(
            http_method="ANY",
            authorization_type=api_gtwy.AuthorizationType(
                api_gtwy.AuthorizationType.IAM
            ),
            integration=details_fn_integration,
        ).grant_execute(cognito_idp.authenticated_role)

        web_deployment.add_source(
            s3_deployment.Source.data(
                "aws-config.js",
                """
const awsmobile = {
    aws_project_region: '"""
                + aws_cdk.Stack.of(self).region
                + """',
    aws_cognito_region: '"""
                + aws_cdk.Stack.of(self).region
                + """',
    aws_cognito_identity_pool_id:'"""
                + cognito_idp.identity_pool_id
                + """',
    aws_user_pools_id:'"""
                + user_pool.user_pool_id
                + """',
    aws_user_pools_web_client_id: '"""
                + cognito_app_client.user_pool_client_id
                + """',
    aws_cognito_username_attributes: ['EMAIL'],
    aws_cognito_mfa_configuration: 'OFF',
    aws_cognito_password_protection_settings: {
        passwordPolicyMinLength: 8,
        passwordPolicyCharacters: ['REQUIRES_LOWERCASE', 'REQUIRES_UPPERCASE', 'REQUIRES_NUMBERS', 'REQUIRES_SYMBOLS'],
    },
    aws_cognito_verification_mechanisms: ['EMAIL'],
    API: {
        endpoints: [
            {
                name: 'ci-api',
                endpoint: '"""
                + rest_api.url[:-1]
                + """',
            },
        ],
    }
};
window.aws_config = awsmobile;
            """,
            )
        )

        CfnOutput(
            self,
            "distribution",
            value=distribution.domain_name,
            export_name="llm-ins-distribution",
        )
        CfnOutput(
            self,
            "cfn_api_gateway",
            value=rest_api.url,
            export_name="api-gateway",
        )
        CfnOutput(
            self,
            "cfn_user_pool_client_id",
            value=cognito_app_client.user_pool_client_id,
            export_name="user-pool-client-id",
        )
        CfnOutput(
            self,
            "cfn_user_pool_id",
            value=user_pool.user_pool_id,
            export_name="user-pool-id",
        )
        CfnOutput(
            self,
            "cfn_identity_provider_id",
            value=cognito_idp.identity_pool_id,
            export_name="identity-provider-id",
        )
