import json
import os

import boto3
from dotenv import load_dotenv
from pulumi import automation as auto

from cloudaciousIAC import AWS
from cloudaciousIAC.ContainerImages import Image
from cloudaciousIAC.StackInfo import StackInfo

load_dotenv()


def main(event, context):
    """
    Rebuilds the container image for an AWS Lambda function created using `./webhook.py` using Pulumi Automation API, pushes it to AWS ECR, and updates the Lambda function to the new container.
    """
    #########
    ### AWS+Config
    #########
    aws_region_name = os.getenv("AWS_REGION")
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_session_token = os.getenv("AWS_SESSION_TOKEN")
    session = boto3.Session(
        region_name=aws_region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
    )
    #########
    ### stack_info -> this session's vars
    #########
    stack_action = event["stack_action"]
    stack_info = event["stack_info"]
    stack_name = stack_info["stack_name"]
    aws_account_id = stack_info["cloud_config"]["aws_account_id"]
    fn_purpose = event["fn_purpose"]
    client = stack_info["client_config"]["client"]
    pulumi_backend_url = stack_info["pulumi_backend_url"]

    ### init stack info
    stack_info_class = StackInfo(stack_info)
    # get img cfg
    image_config = stack_info_class.image_config(fn_purpose)

    ### init AWS class

    aws_ = AWS.AWS(session=session)
    # get ecr auth token
    auth_token = aws_.ecr_token(aws_account_id=aws_account_id)

    ### init image class
    image = Image(
        image_config=image_config,
        auth_token=auth_token,
    )

    #########
    ### debugging
    #########
    print(f"{__name__}: pulumi_backend_url: {pulumi_backend_url}")
    print(f"{__name__}: stack_action: {stack_action}")
    print(f"{__name__}: stack_info: {stack_info}")
    print(f"{__name__}: stack_name: {stack_name}")
    print(f"{__name__}: aws_account_id: {aws_account_id}")
    print(f"{__name__}: fn_purpose: {fn_purpose}")
    print(f"{__name__}: client: {client}")
    print(f"{__name__}: stack_info_class: {stack_info_class}")
    print(f"{__name__}: image_config: {image_config}")

    ##########
    ### Pulumi
    ##########
    project_settings = auto.ProjectSettings(
        name=f"{stack_name}",
        runtime="python",
        backend={"url": pulumi_backend_url},
    )

    ### init stack
    stack = auto.create_or_select_stack(
        stack_name="production",
        project_name=f"{stack_name}",
        program=image.create_image,
        opts=auto.LocalWorkspaceOptions(project_settings=project_settings),
    )
    stack.set_config("aws:region", auto.ConfigValue("us-east-1"))

    # deploy the stack, tailing the logs to stdout
    if stack_action == "up":
        up_res = stack.up(on_output=print)

        # get export of image name from `Image` class
        base_image_name = up_res.outputs["base_image_name"].value
        # use boto3 to update lambda fn to new image
        aws_.update_lambda_function(base_image_name=base_image_name)
    elif stack_action == "destroy":
        up_res = stack.destroy(on_output=print)

    elif stack_action == "cancel":
        res = stack.cancel(on_output=print)
    else:
        print(
            f"{__name__}: stack action up/destroy invalid, stack_action is: {stack_action}"
        )
    return


if __name__ == "__main__":
    event = {}
    # run Pulumi
    main(event=event, context="")
