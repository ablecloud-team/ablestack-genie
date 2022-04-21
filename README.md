# ABLESTACK Genie
ABLESTACK 클라우드 인프라 및 애플리케이션 배포 자동화 플랫폼

## Automation Controller 템플릿 구성 방법

### Automation Controller 구성 정보
Docker 기반의 MiniKube를 사용하고 Single Node 아키텍처를 적용합니다.
- OS: CentOS 8.5 2111
- 요구 사항:
  - Genie VM: 8Core 16G
  - Minikube Cluster: 4Core 8G

### automation_controller_installation.sh 실행
임의의 경로 또는 "$ /genie/" 에 설치에 필요한 파일들을 위치합니다.
```
$ ls -al

install_automation_controller_vm.sh         # Automation Controller 템플릿을 구성하기 위한 환경 설정
automation_controller_installation.yml      # Automation Controller 템플릿을 구성 플레이북
check_port_forward.service                  # k8s 포트포워딩 상태 체크 서비스
check_port_forward.sh                       # k8s 포트포워딩 상태 체크 서비스의 쉘 프로그램
automation_controller_initialization.yml    # 템플릿이 사용자에 의해 구성될 때 

```

### Install Docker
```
$ dnf -y remove podman buildah
$ dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
$ dnf -y install docker-ce docker-ce-cli containerd.io
$ systemctl enable docker
$ systemctl start docker
```

### Install minikube
```
$ curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
$ install minikube-linux-amd64 /usr/local/bin/minikube
```

### Install kubectl
```
$ curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
$ install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

### Install awx-operator
- 쿠버네티스 클러스터 환경에서 AWX를 쉽게 배포하기 위한 도구입니다.
```
$ git clone https://github.com/ansible/awx-operator.git 
$ cd awx-operator
$ git checkout 0.17.0
```

### Add Firewall Rules
```
$ firewall-cmd --permanent --zone=public --add-service=http
$ firewall-cmd --permanent --zone=public --add-port=8001/tcp
$ firewall-cmd --reload
```

### Config sshd
```
$ vi /etc/ssh/sshd_config
  PasswordAuthentication yes
  PermitRootLogin yes
$ systemctl restart sshd
```

### Config cloud-init
```
$ vi /etc/cloud/cloud.cfg
  disable_root: false
  ssh_pwauth: true
```

### Start minikube
- AWX를 사용하기 위한 도커 기반의 쿠버네티스 클러스터를 생성합니다.
```
$ minikube start --cpus=4 --memory=8g --addons=ingress --install-addons=true --driver=docker --force
```

쿠버네티스 클러스터가 정상적으로 생성되었는 지 확인합니다.
```
$ minikube kubectl -- get nodes
$ minikube kubectl -- get pods -A
```

minikube에 내장된 kubectl를 사용하도록 변경하고 namespace 변수를 등록합니다.
```
$ alias kubectl="minikube kubectl --"
$ export NAMESPACE=awx
```

AWX Operator를 쿠버네티스 클러스터에 배포합니다.
```
$ make deploy
```

AWX Operator pod가 정상적으로 배포 되었는지 확인합니다. awx-operator-controller의 상태가 'Running'이 된 후 다음 단계를 진행합니다.
```
$ kubectl get pods -n awx

NAME                                               READY   STATUS    RESTARTS   AGE
awx-operator-controller-manager-66ccd8f997-rhd4z   2/2     Running   0          11s
```

기본 namespace를 `awx`로 변경합니다.
```
$ kubectl config set-context --current --namespace=awx
```

AWX Deployment와 Service를 생성하기 위한 yml파일을 변경합니다.  

`$ vi awx-demo.yml` 
```yaml
---
apiVersion: awx.ansible.com/v1beta1
kind: AWX
metadata:
  name: awx
spec:
  service_type: nodeport
  ingress_type: none
  projects_persistence: true
```
- AWX Deployment와 Service 내용을 변경하려면 `main.yml`를 참조합니다.
  -  https://github.com/ansible/awx-operator/blob/devel/roles/installer/defaults/main.yml
<br>
<br>

`awx-demo.yml` 내용에 따라 배포합니다. 이 작업은 약 2분 소요됩니다. 
```
$ kubectl apply -n awx -f awx-demo.yml
```

생성된 pod를 확인합니다.
```
$ kubectl get pods -n awx -l "app.kubernetes.io/managed-by=awx-operator"

NAME                        READY   STATUS    RESTARTS   AGE
awx-77d96f88d5-pnhr8        4/4     Running   0          3m24s
awx-postgres-0              1/1     Running   0          3m34s
```

생성된 service를 확인합니다.
```
$ kubectl get svc -n awx -l "app.kubernetes.io/managed-by=awx-operator"

NAME                TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
awx-postgres        ClusterIP   None           <none>        5432/TCP       4m4s
awx-service         NodePort    10.109.40.38   <none>        80:31006/TCP   3m56s
```

외부에서 AWX 대시보드 접근을 위한 포트포워딩을 백그라운드에서 실행합니다.
```
$ kubectl port-forward svc/awx-service -n awx --address 0.0.0.0 80:80 &> /dev/null &
```

admin password 추출
 - 기본적으로 admin 사용자는 admin이고 암호는 <resourcename>-admin-password시크릿에서 추출할 수 있습니다. 관리자 암호를 검색하려면 다음을 실행합니다.
```
$ kubectl get -n awx secret awx-admin-password -o jsonpath="{.data.password}" | base64 --decode 
```

AWX 대시보드에 접속합니다.
- http://<<public_ip>>:80
- ID/PW : admin/PASSWORD
  
![image](https://user-images.githubusercontent.com/34114265/158306866-95408b73-cfac-4682-9b7c-dafd83b4ddbd.png)


#
### 쿠버네티스 클러스터 관리 대시보드 설치
- minikube 명령어로 클러스터 대시보드 에드온을 설치합니다.
```
$ minikube addons enable dashboard
$ kubectl proxy --address='0.0.0.0' --disable-filter=true  &> /dev/null &
```
- public ip를 변경한 후 접속합니다.
  - http://<<public_ip>>:8001/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/ 

![image](https://user-images.githubusercontent.com/34114265/158307186-c816ab72-6484-44ac-91f2-d6bd815a2177.png)







