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

SCRIPTS_DIR="$(dirname "${BASH_SOURCE[0]}")"
INSTALL_DIR="$(realpath $(dirname ${BASH_SOURCE[0]})/..)"

# make sure we're running as the owner of the checkout directory
RUN_AS="$(ls -ld "$SCRIPTS_DIR" | awk 'NR==1 {print $3}')"
if [ "$USER" != "$RUN_AS" ]
then
    echo ""
    echo " This script must run as $RUN_AS, trying to change user..."
    exec sudo -u $RUN_AS $0
fi
echo ""
echo " Updating your system..."
echo ""
sudo apt-get update -y
sed 's/#.*//' ${INSTALL_DIR}/requirements/system-requirements.txt | xargs sudo apt-get install -y
cd /home/${USER}/

echo ""
echo " Create virtual enviroment..."
echo ""
python3 -m venv ${INSTALL_DIR}/env
${INSTALL_DIR}/env/bin/python -m pip install --upgrade pip setuptools wheel
source ${INSTALL_DIR}/env/bin/activate

echo ""
echo " Installing python packages..."
echo ""
pip3 install -r ${INSTALL_DIR}/requirements/pip-requirements.txt
