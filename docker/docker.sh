#!/bin/bash

DOCKER_IMAGE="neuchips/viper_prod:v1.2"

CMD=$1

if [ -z $CMD ]; then
    echo
    echo "Usage:"
    echo " $0 build"
    echo " $0 stop <env_file>"
    echo " $0 run <env_file>"
    echo
    exit 0
fi

shift

case $CMD in
    build)
        docker build -f ./Dockerfile -t ${DOCKER_IMAGE} .. --no-cache --rm
        ;;
    stop)
        if [ -z $1 ]; then
            ENV="env_llama3"
        else
            ENV="$1"
        fi

        source $ENV

        docker stop ${CONTAINER_NAME}
        ;;
    run)
        if [ -z $1 ]; then
            ENV="env_llama3"
        else
            ENV="$1"
        fi

        source $ENV

        docker run -d -it --privileged --rm -w=/neuchips/ \
            --name ${CONTAINER_NAME} \
            -v /dev:/dev \
            -p $PORT:$PORT \
            --env-file $ENV \
            -v ${HOST_MODEL_FOLDER}:${DOCKER_MODEL_FOLDER} \
            -v ${HOST_CACHE_FOLDER}:${DOCKER_CACHE_FOLDER} \
            ${DOCKER_IMAGE}
        ;;
    test)
        if [ -z $1 ]; then
            ENV="env_llama3"
        else
            ENV="$1"
        fi

        source $ENV

        curl -v --request POST \
             --url http://localhost:${PORT}/completion \
             --header "Authorization: Bearer ${API_KEY}" \
             --header "Content-Type: application/json" \
             --data '{
                "prompt": "Wikipedia is",
                "max_tokens": 16
             }'
        ;;
    *)
esac
