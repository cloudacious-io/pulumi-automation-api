#!/bin/bash

export $(grep -v '^#' .env | xargs)

docker build --build-arg CI_COMMIT_TAG=$CI_COMMIT_TAG --build-arg CLOUDACIOUS_IAC_REPO_URL=$CLOUDACIOUS_IAC_REPO_URL --build-arg CLOUDACIOUS_IAC_REPO_BRANCH=$CLOUDACIOUS_IAC_REPO_BRANCH --build-arg GITLAB_TOKEN_USER=$GITLAB_TOKEN_USER --build-arg GITLAB_TOKEN=$GITLAB_TOKEN -t meep-morp-bot-infra . --progress=plain --no-cache

docker run --rm -it --name meep-morp-bot-infra --volume $(pwd)/:/code -v /var/run/docker.sock:/var/run/docker.sock meep-morp-bot-infra bash
