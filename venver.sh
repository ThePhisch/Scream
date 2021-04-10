#!/bin/bash
# Prepare environment for Scream

# Install packages
# $REQUIRED_PKGS is an array with the required packages
REQUIRED_PKGS=("python3-pip" "python3-venv")
for p in "${REQUIRED_PKGS[@]}"; do
    PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $p | grep "install ok installed")
    echo "Checking for $p: $PKG_OK"

    if [[ -z $PKG_OK ]]; then
        echo "$p not found, will install now"
        sudo apt install $p
    fi
done
echo "All packages installed, continue to creation of venv"

# Create Venv
ENV_NAME="screamenv"
echo "Create Virtual Environment with the name $ENV_NAME"
python3 -m venv $ENV_NAME

# Enter Venv, install pip packages
# once done with venv, leave venv
PYTHON_PKGS=("Flask" "gunicorn" "wheel")
echo "entering $ENV_NAME, installing pip packages"
source $ENV_NAME/bin/activate
for p in "${PYTHON_PKGS[@]}"; do
    pip install $p
done
echo "done with $ENV_NAME"
deactivate

# deal with environment variables
# check if all required ones are defined (not empty)
# otherwise highlight in bold red
# and give a hint on where to define them
REQUIRED_ENVVARS=("DB_USER" "DB_PASS")
ANYERROR=0
echo -e "\n===== Environment Variables ====="
for p in ${REQUIRED_ENVVARS[@]}; do
    if [[ -n $(printenv $p) ]]; then
        echo "$p set and ready to go"
    else
        # error in red
        tput setaf 1; tput bold; echo "$p not set"; tput sgr0
        ANYERROR=1
    fi
done
echo -e "===== ===================== ====="
if [[ $ANYERROR == 1 ]] ; then
    tput setaf 1; tput bold; echo "errors encountered in environment variables"; tput sgr0
    echo "suggestion: add variables to /etc/environment"
fi
echo "done"
