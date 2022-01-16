from ..input_outputs import AWSHttpAPIGateway as AWSInputOutput
from clearskies.contexts.build_context import build_context
from clearskies.contexts.context import Context
class AwsHttpAPIGateway(Context):
    def __init__(self, di):
        super().__init__(di)

    def __call__(self, event, context):
        if self.handler is None:
            raise ValueError("Cannot execute AWSLambda context without first configuring it")

        return self.handler(AWSInputOutput(event, context))
def aws_http_api_gateway(
    application,
    di_class=None,
    bindings=None,
    binding_classes=None,
    binding_modules=None,
    additional_configs=None,
):
    return build_context(
        AWSLambdaHTTPAPIGateway,
        application,
        di_class=di_class,
        bindings=bindings,
        binding_classes=binding_classes,
        binding_modules=binding_modules,
        additional_configs=additional_configs,
    )
