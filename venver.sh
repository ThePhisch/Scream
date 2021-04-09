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
PYTHON_PKGS=("Flask")
echo "entering $ENV_NAME, installing pip packages"
source $ENV_NAME/bin/activate
for p in "${PYTHON_PKGS[@]}"; do
    python3 -m pip install $p
done
echo "done with $ENV_NAME"
deactivate
echo "done"