# Prepare environment for Scream

# Install packages
REQUIRED_PKG="python3-pip"
PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG | grep "install ok installed")
echo "Checking for $REQUIRED_PKG : $PKG_OK"

if [[ -z $PKG_OK ]]; then
    echo "$REQUIRED_PKG not found, will install now"
    sudo apt install $REQUIRED_PKG
fi

# Create Venv