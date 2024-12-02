#!/bin/sh
echo "starting installation script"

echo "update and install apt packages"
sudo apt update
sudo apt upgrade -y
sudo apt install -y vim iputils-ping dos2unix

echo "install and start ssh"
sudo apt install -y ssh
sudo service ssh restart

echo "setting up Rob public key for ssh access"
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCeYYGvQ4QUQm8mS/VvT3rvlHx1EibqSjDpjC9dTBds0COpZFIc+pCMbT7a3tNeR9/6+ODZotcGX0oDjemIW/d98/8fMOKaTbAC7zNY6DyV0rOhXsf/9FCa97vxhnaVejfWTmTl2cljfuXC0nhfmoOB6oOt7NyiGXGMrwYyLIZG8GkAPLlrG/HRBHr8sO5Vr4scd2EjwYLjWtHr0agvCVD20jN3AA6KzszRMhgl9sVrswSwxe+vt8cJoP0ooUXM7kc7/CYDgIcC86GHGR0vzXeF4rrtIArfUPC59WET8Z9+IKwySL5v7R+Y7yi88PR9sABqBXqOzN+kciKCsb/xfL8VhQXlI1+Jb12pFP4h3nSwDIW/5S3697t3vc0vo0jjzXIoHumbQ2w1YLoGdvTcWaKFY3vDFfC0fHywsCj7RNLzTZLqQ4r5YS5EgNvt5RiMiAClwADZ8wZHBOtbVKDWK++9nHGISrgIh1Dehlj0oeAQz6+s5fI9TGp3oB8nEx5tEgs= openssh-rsa-key-20210222-rob-anomaly" >> ~/.ssh/authorized_keys

echo "create virtual environment"
python3 -m venv .venv

echo "activate virtual environment" 
source .venv/bin/activate

echo "upgrade pip"
python -m pip install -U pip

echo "install requirements"
pip install -r requirements.txt

echo "installation script complete"