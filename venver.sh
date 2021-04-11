#!/bin/bash
# Prepare environment for Scream
GIVEN_VNAME="v0.1.zip"
# Loop to process input
while [[ -n $1 ]]; do # while loop
    case $1 in
        -v)
            # Pass name of version to download
            GIVEN_VNAME="$2"
            echo "Will download version $GIVEN_VNAME"
            shift
            ;;
        -sa)
            # Suppress linux package check 
            FLAG_LINUX_PACKAGE_CHECK=0
            ;;
        -sv)
            # Suppress venv creation
            FLAG_VENV_CREATION=0
            ;;
        -sp)
            # Suppress python package check
            FLAG_PYTHON_PACKAGE_CHECK=0
            ;; 
        -sP)
            # sv and sp
            FLAG_VENV_CREATION=0
            FLAG_PYTHON_PACKAGE_CHECK=0
            ;; 
        -se)
            # Suppress environment vars
            FLAG_ENVIRONMENT_VARS=0
            ;;
        -su)
            # Suppress version update
            FLAG_VERSION_UPDATE=0
            ;; 
        *) echo "option $1 not recognized" ;;
    esac
    shift
done

if [[ -z $FLAG_LINUX_PACKAGE_CHECK ]]; then
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
else
    echo "Skipped checking Linux Packages"
fi

if [[ -z $FLAG_VENV_CREATION ]]; then
    # Create Venv
    ENV_NAME="screamenv"
    echo "Create Virtual Environment with the name $ENV_NAME"
    python3 -m venv $ENV_NAME
else
    echo "Skipped Creation of venv"
fi
if [[ -z $FLAG_PYTHON_PACKAGE_CHECK ]]; then
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
else
    echo "Skipped Python Package check"
fi
if [[ -z $FLAG_ENVIRONMENT_VARS ]]; then
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
    echo -e "===== ===================== =====\n"
    if [[ $ANYERROR == 1 ]] ; then
        tput setaf 1; tput bold; echo "errors encountered in environment variables"; tput sgr0
        echo "suggestion: add variables to /etc/environment"
    fi
else
    echo "skipped environment variable check"
fi

if [[ -z $FLAG_VERSION_UPDATE ]]; then
    # Download release from github, delete previous files and replace them
    GITHUB_SOURCE="https://github.com/ThePhisch/Scream/archive/refs/tags/"
    DOWNLOAD_LINK="$GITHUB_SOURCE$GIVEN_VNAME"
    echo "getting from $DOWNLOAD_LINK"
    wget -O dload $DOWNLOAD_LINK
    unzip dload
    NAME_OF_FOLDER=$(ls -l | grep Scream- | awk '{print $NF}')
    STUFF_TO_REPLACE=("wsgi.py" "spp/")
    if [[ -n $NAME_OF_FOLDER ]]; then
        tput bold; echo "The unzipped folder's name is $NAME_OF_FOLDER"; tput sgr0
        for p in ${STUFF_TO_REPLACE[@]}; do
            echo "Replacing $p"
            rm -rf $p
            mv $NAME_OF_FOLDER/$p $p
        done
        rm -rf $NAME_OF_FOLDER/
    else
        tput setaf 1; tput bold; echo "There was an issue with the download"; tput sgr0
    fi
    echo "Cleaning: removing dload"
    rm dload
else
    echo "No Download command given, nothing downloaded or replaced"
fi


echo "done"

# Now:
# Run with gunicorn, e.g. gunicorn wsgi:app
# Connect gunicorn with Nginx
