#!/bin/bash

help() {
    echo
    echo "Usage:"
    echo " $0 build [REPOSITORY_NAME/TAG        (default: $DOCKER_IMAGE)]"
    echo " $0 stop ENV_FILE"
    echo " $0 run ENV_FILE"
    echo " $0 test ENV_FILE -p PROMPT(or -f PROMPT_TXT_FILE) [MAX_TOKENS        (default: $MAX_TOKENS)]"
    echo
    exit 0
}

DOCKER_IMAGE="neuchips/viper_prod:v1.4.2-alpha.1"
ENV="env_llama3_8b"
MAX_TOKENS=128

CMD="$1"

if [ -z "$CMD" ] || [ "$CMD" == "-h" ] || [ "$CMD" == "--help" ]; then
    help
fi

shift

case "$CMD" in
    build)
        if [ -z "$1" ]; then
            read -p "Use default repository name/tag: $DOCKER_IMAGE? (y/n)" ANS
            if [[ -n "$ANS" && ("$ANS" == n || "$ANS" == N) ]]; then
                read -p "Enter repository name/tag: " DOCKER_IMAGE
            fi
        else
            DOCKER_IMAGE="$1"
        fi
        docker build -f ./Dockerfile -t "${DOCKER_IMAGE}" .. --no-cache --rm
        ;;
    stop)
        if [ $# -ne 1 ]; then
            help
        fi

        ENV="$1"
        source "$ENV"

        docker stop "${CONTAINER_NAME}"
        ;;
    run)
        if [ $# -ne 1 ]; then
            help
        fi

        ENV="$1"
        source "$ENV"

        docker run -d -it --privileged --rm -w=/neuchips/ \
            --name "${CONTAINER_NAME}" \
            -v /dev:/dev \
            -p "$PORT":"$PORT" \
            --env-file "$ENV" \
            -v "${HOST_MODEL_FOLDER}":"${DOCKER_MODEL_FOLDER}" \
            -v "${HOST_CACHE_FOLDER}":"${DOCKER_CACHE_FOLDER}" \
            "${DOCKER_IMAGE}" \
        ;;
    test)
        if [ $# -lt 3 ] || [ $# -gt 4 ]; then
            help
        fi

        ENV="$1"
        source "$ENV"

        if [ -n "$4" ]; then
            MAX_TOKENS="$4"
        fi

        if [ "$2" == "-p" ]; then
            PROMPT="$3"
        elif [ "$2" == "-f" ]; then
            PROMPT=$(cat "$3")
        else
            help
        fi

        curl -v --request POST \
             --url "http://localhost:${PORT}/completion" \
             --header "Authorization: Bearer ${API_KEY}" \
             --header "Content-Type: application/json" \
             --data @- <<EOF
             {
                "prompt": "$PROMPT",
                "max_tokens": $MAX_TOKENS
             }
EOF
        ;;
    *)
esac
