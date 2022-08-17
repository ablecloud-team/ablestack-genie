#!/bin/sh

### Variables
ANSIBLE_VERSION="2.12.2-2.el8"

EPEL_VERSION="8-11.el8"

COLLECTION_GENERAL_VERSION="4.6.1"
PIP3_JMESPATH_VERSION="1.0.0"

COLLECTION_DOCKER_VERSION="2.3.0"
PIP3_DOCKER_VERSION="5.0.3"

### 환경변수 설정
HERE=$(dirname $(realpath $0))

### Setting Repositories
# sed -i 's/mirrorlist/#mirrorlist/' /etc/yum.repos.d/CentOS*
# sed -i 's/#baseurl=http:\/\/mirror\.centos\.org/baseurl=http:\/\/mirror.ablecloud.io/' /etc/yum.repos.d/CentOS*
# sed -i 's/$releasever/8-stream/' /etc/yum.repos.d/CentOS*
# mkdir /etc/yum.repos.d/unused
# mv /etc/yum.repos.d/CentOS-Linux-Media* /etc/yum.repos.d/unused/
# mv /etc/yum.repos.d/CentOS-Linux-FastTrack.repo /etc/yum.repos.d/unused/


### Install Ansible and collections
#dnf -y update --allowerasing
dnf -y install epel-release-$EPEL_VERSION
dnf -y install ansible-core-$ANSIBLE_VERSION
ansible-galaxy collection install community.general:==$COLLECTION_GENERAL_VERSION
pip3 install jmespath==$PIP3_JMESPATH_VERSION
ansible-galaxy collection install community.docker:==$COLLECTION_DOCKER_VERSION
pip3 install docker==$PIP3_DOCKER_VERSION


### AWX-EE 이미지 변경 Playbook 실행
ansible-playbook $HERE/customize_awx_ee.yml