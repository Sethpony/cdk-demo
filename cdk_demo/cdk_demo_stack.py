from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,  # using _lambda because lambda is a built-in identifier in Python
    aws_apigateway as apigw
)
#import the construct we created
from .hitcounter import HitCounter


# This is a class that represents the CFN stack
class CdkDemoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Defines an AWS Lambda Resource
        my_lambda = _lambda.Function(
            self, 'HelloHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            # where the code resides - alternative path definition code=lambda_.Code.from_asset(path.join(__dirname, "my-lambda-handler")),

            handler='hello.handler',
            # The name of the handler function is hello.handler, 'hello' is the name of the file and 'handler' is the function name
        )

        # defining the hitcounter construct we created
        hello_with_counter = HitCounter(
            self, 'HelloHitCounter',
            downstream=my_lambda,
        )

        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=hello_with_counter._handler,
            # create an endpoint and run the lambda function
        )
