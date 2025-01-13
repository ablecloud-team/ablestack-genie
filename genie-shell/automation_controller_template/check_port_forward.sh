#!/bin/bash

while [ 1 ]
do
    STATUS=$(curl -o /dev/null -w "%{http_code}" "http://localhost:8075")
    pid_dashboard=`ps -ef | grep "kubectl port-forward svc/awx-service" | grep -v 'grep' | awk '{print $2}'`
    pid_postgres=`ps -ef | grep "kubectl port-forward svc/awx-postgres" | grep -v 'grep' | awk '{print $2}'`
    pid_proxy=`ps -ef | grep "kubectl proxy" | grep -v 'grep' | awk '{print $2}'`

    if [ $STATUS -ne 200 ]
    then
        kill `ps -ef | grep 'kubectl port-forward' | grep -v grep | awk '{print $2}'`
    fi

    if [ -z $pid_dashboard ]
    then
        nohup kubectl port-forward svc/awx-service -n awx --address 0.0.0.0 8075:8075 &> /dev/null &
    fi

    if [ -z $pid_postgres ]
    then
        nohup kubectl port-forward svc/awx-postgres -n awx --address 0.0.0.0 5432:5432 &> /dev/null &
    fi

    if [ -z $pid_proxy ]
    then
        nohup kubectl proxy --address='0.0.0.0' --disable-filter=true  &> /dev/null &
    fi
    
    sleep 2
done