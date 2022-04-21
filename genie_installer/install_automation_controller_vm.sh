#!/bin/sh

### Variables
ANSIBLE_VERSION="2.12.2-2.el8"

EPEL_VERSION="8-11.el8"

COLLECTION_GENERAL_VERSION="4.6.1"
PIP3_JMESPATH_VERSION="1.0.0"

COLLECTION_CS_VERSION="2.2.3"
PIP3_CS_VERSION="3.0.0"
PIP3_SSHPUBKEYS_VERSION="3.3.1"

COLLECTION_AWX_VERSION="20.1.0"

COLLECTION_CRYPTO_VERSION="2.2.4"


### 환경변수 설정
HERE=$(dirname $(realpath $0))

### Repositories 설정
sed -i 's/mirrorlist/#mirrorlist/' /etc/yum.repos.d/CentOS*
sed -i 's/#baseurl=http:\/\/mirror\.centos\.org/baseurl=http:\/\/mirror.ablecloud.io/' /etc/yum.repos.d/CentOS*
sed -i 's/$releasever/8-stream/' /etc/yum.repos.d/CentOS*
mkdir /etc/yum.repos.d/unused
mv /etc/yum.repos.d/CentOS-Linux-Media* /etc/yum.repos.d/unused/
mv /etc/yum.repos.d/CentOS-Linux-FastTrack.repo /etc/yum.repos.d/unused/


### Ansible and collections 설치
#dnf -y update --allowerasing
dnf -y install epel-release-$EPEL_VERSION
dnf -y install ansible-core-$ANSIBLE_VERSION
ansible-galaxy collection install community.general:==$COLLECTION_GENERAL_VERSION
pip3 install jmespath==$PIP3_JMESPATH_VERSION
ansible-galaxy collection install ngine_io.cloudstack:==$COLLECTION_CS_VERSION
pip3 install cs==$PIP3_CS_VERSION
pip3 install sshpubkeys==$PIP3_SSHPUBKEYS_VERSION
ansible-galaxy collection install awx.awx:==$COLLECTION_AWX_VERSION
ansible-galaxy collection install community.crypto:==$COLLECTION_AWX_VERSION

### Check Port Forward Service 설정
sed -i 's/^SELINUX=enforcing/SELINUX=permissive/' /etc/selinux/config
setenforce 0

mkdir -p /genie/check_port_forward
cp $HERE/check_port_forward.sh /genie/check_port_forward/
cp $HERE/check_port_forward.service /etc/systemd/system/check_port_forward.service
chmod -R 755 check_port_forward
systemctl daemon-reload
systemctl enable check_port_forward

### Genie VM 템플릿 배포 Playbook 실행
ansible-playbook $HERE/automation_controller_installation.yml