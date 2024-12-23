#!/bin/bash
echo "============== install pcie driver BEGIN =============="

DRIVER_PATH=""
INSTALL_MODE="online"
DEFAULT_IP="10.1.1.13"

function display_help
{
    echo "Usage: $0 [--url=ip|--file=path]"
}

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --url=*)
            if [ ! -z "${DRIVER_PATH}" ]; then
                echo "Error: Both --url and --file options are specified. Please choose one."
                exit 1
            fi
            DRIVER_PATH="${1#*=}"
            ;;
        --file=*)
            if [ ! -z "${DRIVER_PATH}" ]; then
                echo "Error: Both --url and --file options are specified. Please choose one."
                exit 1
            fi
            DRIVER_PATH="${1#*=}"
            INSTALL_MODE="offline"
            ;;
	--help)
            display_help
            exit 0
            ;;
        *)
            echo "Unknown parameter passed: $1";
            display_help
            exit 1
            ;;
    esac
    shift
done

if [ "${INSTALL_MODE}" = "online" ]; then
    if [ -z "${DRIVER_PATH}" ]; then
        DRIVER_PATH="${DEFAULT_IP}"
        echo "Use default ip address ${DEFAULT_IP}"
    fi

    /bin/bash -c "$(curl -fsSL http://${DRIVER_PATH}/apt-env.sh)"
    sudo apt install neuchips-pcie-modules
elif [ "${INSTALL_MODE}" = "offline" ]; then
    if [ -z "${DRIVER_PATH}" ]; then
        echo "Error: --file option requires a valid file path."
        display_help
        exit 1
    fi

    sudo dpkg -i ${DRIVER_PATH}/neuchips-pcie-modules_*.deb
else
    display_help
    exit 1
fi
echo "============== install pcie driver END =============="

cat /sys/module/neuchips_ai_ep/parameters/driver_ver
