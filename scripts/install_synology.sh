#!/bin/bash
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
set -o errexit

NAME="Domoticz-Google-Assistant"
INSTALL_DIR="$(realpath $(dirname ${BASH_SOURCE[0]})/..)"
ROOT_DIR="$(realpath $(dirname ${BASH_SOURCE[0]})/../..)"
output="dzga.conf"

if [ ! -d ${INSTALL_DIR} ]; then
	echo ""
	echo " Can't find Domoticz-Google-Assistant folder!"
	echo ""
	exit 1
fi
echo " *--------------------**---------------------*"
echo " Installation for Synology"
echo " ---------------------------------------------"
echo " *Note : Domoticz-Google-Assistant is free"
echo " *for personal use."
echo " ---------------------------------------------"
echo ""
if ! hash python3; then
    echo " Python3 is not installed"
    exit 1
fi
ver=$(python3 -V 2>&1 | sed 's/.* \([0-9]\).\([0-9]\).*/\1\2/')
if [ "$ver" -lt "35" ]; then
    echo " $NAME requires python 3.5 or greater"
	echo ""
    exit 1
fi
echo "Continue?"
echo "(y)es or (N)o?"
read choice
if [ "$choice" = "N" ] || [ "$choice" = "n" ]; then
	echo "User abort installation"
	exit 0
fi
echo ""
echo " Create virtual enviroment..."
echo ""
#python3 -m venv ${INSTALL_DIR}/env
#${INSTALL_DIR}/env/bin/python -m pip install --upgrade pip setuptools wheel
source ${INSTALL_DIR}/env/bin/activate

echo ""
echo " Installing python packages..."
echo ""
# pip3 install -r ${INSTALL_DIR}/requirements/pip-requirements.txt

echo ""
echo " Create dzga daemon file"
echo ""
cp ${INSTALL_DIR}/systemd/dzga_synology.service dzga-daemon
sudo chmod 755 dzga-daemon
sudo ${ROOT_DIR}/dzga-daemon restart

# echo ""
# echo " Create conf file"
# echo ""
# echo "# only start this service after the httpd user process has started" | tee -a $output
# echo "start on started httpd-user" | tee -a $output
# echo "" | tee -a $output
# echo "# stop the service gracefully if the runlevel changes to 'reboot'" | tee -a $output
# echo "stop on runlevel [06]" | tee -a $output
# echo "" | tee -a $output
# echo "# run the scripts as the 'http' user. Running as root (the default) is a bad ide" | tee -a $output
# echo "#setuid admin" | tee -a $output
# echo "" | tee -a $output
# echo "# exec the process. Use fully formed path names so that there is no reliance on" | tee -a $output
# echo "# the 'www' file is a node.js script which starts the foobar application." | tee -a $output
# echo "exec /bin/sh $ROOT_DIR/dzga-daemon start" | tee -a $output
# echo "" | tee -a $output	

echo ""
echo "  Login to Domoticz Google Assistant Server UI at: http://ip.address:3030/settings"
echo "  Default username is admin and default password is admin"
echo "  or"
echo "  Goto Domoticz-Google-Assistant folder and Edit config.yaml and then"
echo "  restart dzga.server"
echo ""
echo "  == Useful commands =="
echo "  Start server with command 'sudo ${ROOT_DIR}/dzga-daemon start'"
echo "  Stop server with command 'sudo ${ROOT_DIR}/dzga-daemon stop'"
echo "  Restart server with command 'sudo ${ROOT_DIR}/dzga-daemon restart'"
echo "  Check server status with command 'sudo ${ROOT_DIR}/dzga-daemon status'"
echo ""
