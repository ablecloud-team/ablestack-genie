#!/bin/bash

CMD="$1"

if [ "$CMD" == "start" ] ; then

    ansible-playbook /root/deploy_automation_controller.yml --tag "start minikube"  

elif [ "$CMD" == "stop" ] ; then 

    minikube stop 

elif [ "$CMD" == "status" ] ; then

    minikube status

else

    exit

fi
