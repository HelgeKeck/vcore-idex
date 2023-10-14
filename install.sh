# Prevent running as root.
if [ ${UID} == 0 ]; then
    echo -e "DO NOT RUN THIS SCRIPT AS 'root' !"
    echo -e "If 'root' privileges needed, you will prompted for sudo password."
    exit 1
fi

# Force script to exit if an error occurs
set -e

# Find SRCDIR from the pathname of this script
SRCDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/ && pwd )"

# Default Parameters
MAINSAIL_DIR="${HOME}/mainsail"
CONFIG_DIR="${HOME}/printer_data/config"
KLIPPY_EXTRAS="${HOME}/klipper/klippy/extras"
KLIPPY_KINEMATICS="${HOME}/klipper/klippy/kinematics"

function start_klipper {
    sudo systemctl restart klipper
}

function stop_klipper {
    if [ "$(sudo systemctl list-units --full -all -t service --no-legend | grep -F "klipper.service")" ]; then
        sudo systemctl stop klipper
    else
        echo "Klipper service not found, please install Klipper first"
        exit 1
    fi
}

function link_custom_folder {
    if [ -d "${CONFIG_DIR}" ]; then
        if [ -d "${CONFIG_DIR}/custom" ]; then
            echo -e "${CONFIG_DIR}/custom already exists, skipping..."
        else
            ln -s ${SRCDIR}/klipper_config/custom ${CONFIG_DIR}/custom
            echo -e "custom folder linked"
        fi
    else
        echo -e "ERROR: ${CONFIG_DIR} not found."
        exit 1
    fi
}

function copy_variables_file {
    if [ -d "${CONFIG_DIR}" ]; then
        if [ ! -e "${CONFIG_DIR}/ratos-variables.cfg" ]
        then
            cp "${SRCDIR}/klipper_config/ratos-variables.cfg" "${CONFIG_DIR}/ratos-variables.cfg"
            echo -e "variables file copied"
        fi
    else
        echo -e "ERROR: ${CONFIG_DIR} not found."
        exit 1
    fi
}

function copy_board_files {
    if [ -d "${CONFIG_DIR}" ]; then
        sudo cp -av "${SRCDIR}/klipper_config/RatOS/boards/btt-ebb42-12b" "${CONFIG_DIR}/RatOS/boards"
        echo -e "BTT EBB42 V1.2 board files copied"
    else
        echo -e "ERROR: ${CONFIG_DIR} not found."
        exit 1
    fi
}

function copy_example_cfg {
    if [ -d "${CONFIG_DIR}" ]; then
        cp "${SRCDIR}/klipper_config/printer.cfg" "${CONFIG_DIR}/idex_printer.cfg"
        echo -e "example idex_printer.cfg copied"
    else
        echo -e "ERROR: ${CONFIG_DIR} not found."
        exit 1
    fi
}

function link_klippy_extras {
    if [ -d "${KLIPPY_EXTRAS}" ]; then
        rm -f "${KLIPPY_EXTRAS}/zoffsetprobe.py"
        ln -sf "${SRCDIR}/klippy/extras/zoffsetprobe.py" "${KLIPPY_EXTRAS}/zoffsetprobe.py"
    else
        echo -e "ERROR: ${KLIPPY_EXTRAS} not found."
        exit 1
    fi
}

function link_klippy_kinematics {
    if [ -d "${KLIPPY_KINEMATICS}" ]; then
        rm -f "${KLIPPY_KINEMATICS}/hybrid_corexy.py"
        ln -sf "${SRCDIR}/klippy/kinematics/hybrid_corexy.py" "${KLIPPY_KINEMATICS}/hybrid_corexy.py"
        rm -f "${KLIPPY_KINEMATICS}/idex_modes.py"
        ln -sf "${SRCDIR}/klippy/kinematics/idex_modes.py" "${KLIPPY_KINEMATICS}/idex_modes.py"
    else
        echo -e "ERROR: ${KLIPPY_KINEMATICS} not found."
        exit 1
    fi
}

function copy_modified_release_info {
    if [ -d "${MAINSAIL_DIR}" ]; then
        cp "${SRCDIR}/assets/release_info.json" "${MAINSAIL_DIR}/release_info.json"
        echo -e "modified release_info.json copied"
    else
        echo -e "ERROR: ${MAINSAIL_DIR} not found."
    fi
}

function update_udev_rules {
    if [ -d "${CONFIG_DIR}" ]; then
        sudo ~/printer_data/config/RatOS/scripts/ratos-update.sh
        echo -e "Udev rules updated"
    else
        echo -e "ERROR: ${CONFIG_DIR} not found."
        exit 1
    fi
}

echo -e "V-Core RatOS IDEX"
stop_klipper
link_custom_folder
copy_variables_file
copy_board_files
copy_example_cfg
link_klippy_extras
link_klippy_kinematics
copy_modified_release_info
update_udev_rules
start_klipper
echo -e ""
echo -e "Installation finished!"
echo -e ""
exit 0
