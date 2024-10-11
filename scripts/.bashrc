export PATH=$PATH:/root/.pulumi/bin
export $(cat .env | xargs)

function pulumi_login() {
    pulumi login 's3://${PULUMI_BACKEND_BUCKET}?region=${AWS_REGION}'
}

# set $BRANCH_NAME before using
function reinstall_cloudacious() {
    python -m pip uninstall -y cloudacious
    python -m pip install git+https://${GITLAB_TOKEN_USER}:${GITLAB_TOKEN}@${CLOUDACIOUS_REPO_URL}${CLOUDACIOUS_REPO_BRANCH}
}

function reinstall_cloudacious_main() {
    python -m pip uninstall -y cloudacious
    python -m pip install git+https://${GITLAB_TOKEN_USER}:${GITLAB_TOKEN}@${CLOUDACIOUS_REPO_URL}
}

function reinstall_iac() {
    python -m pip uninstall -y cloudaciousIAC
    python -m pip install git+https://${GITLAB_TOKEN_USER}:${GITLAB_TOKEN}@${CLOUDACIOUS_IAC_REPO_URL}${CLOUDACIOUS_IAC_REPO_BRANCH}
}

function reexport() {
    cd /code
    export $(grep -v '^#' .env | xargs)
    cd -
}

function docker_build() {
    export $(grep -v '^#' .env | xargs)
    docker build --build-arg GITLAB_TOKEN_USER=$GITLAB_TOKEN_USER --build-arg GITLAB_TOKEN=$GITLAB_TOKEN -t meep-morp-bot-infra . --progress=plain --no-cache
}

function docker_run_image() {
    docker run --rm --name meep-morp-bot-infra --volume $(pwd)/:/code -v /var/run/docker.sock:/var/run/docker.sock meep-morp-bot-infra python iac/image.py
}

function docker_run_bot_infra() {
    docker run --rm -it --name meep-morp-bot-infra --volume $(pwd)/:/code -v /var/run/docker.sock:/var/run/docker.sock meep-morp-bot-infra python iac/pulumi_bot_infra.py
}

function docker_run_bash() {
    docker run --rm -it --name meep-morp-bot-infra --volume $(pwd)/:/code -v /var/run/docker.sock:/var/run/docker.sock meep-morp-bot-infra bash
}

function pulumi_image() {
    python iac/image.py
}
