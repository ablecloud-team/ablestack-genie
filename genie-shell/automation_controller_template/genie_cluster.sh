#!/bin/bash

CMD="$1"
pid_proxy=`ps -ef | grep "kubectl proxy" | grep -v 'grep' | awk '{print $2}'`

if [ "$CMD" == "start" ] ; then

    ansible-playbook /root/deploy_automation_controller.yml --tag "start minikube"  

elif [ "$CMD" == "stop" ] ; then 

    minikube stop 

elif [ "$CMD" == "status" ] ; then

    minikube status

else

    exit

fi

if [ -n $pid_proxy ] ; then
    kill -9 $pid_proxy
fi

