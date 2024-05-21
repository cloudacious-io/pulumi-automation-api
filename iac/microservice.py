import os

from dotenv import load_dotenv
from pulumi import automation as auto

from cloudaciousIAC import Microservices

load_dotenv()


def main(event) -> None:
    f"""
    {__name__} creates webhook infrastructure with Pulumi using Pulumi Automation API.
    """

    stack_action = event["stack_action"]
    stack_info = event["stack_info"]
    stack_name = stack_info["stack_name"]
    pulumi_backend_url = stack_info["pulumi_backend_url"]

    project_settings = auto.ProjectSettings(
        name=f"{stack_name}",
        runtime="python",
        backend={"url": pulumi_backend_url},
    )

    microservice = Microservices.Microservice(
        stack_info=stack_info,
    )

    stack = auto.create_or_select_stack(
        stack_name=f"{stack_info['client_config']['client']}",
        project_name=f"{stack_info['stack_name']}",
        program=microservice.microservice,
        opts=auto.LocalWorkspaceOptions(project_settings=project_settings),
    )
    stack.set_config("aws:region", auto.ConfigValue("us-east-1"))

    if stack_action == "up":
        up_res = stack.up(on_output=print)
    elif stack_action == "destroy":
        up_res = stack.destroy(on_output=print)
    else:
        print(
            f"{__name__}: stack action up/destroy invalid, stack_action is: {stack_action}"
        )
    return


if __name__ == "__main__":
    event = {}
    main(event=event)
