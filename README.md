# ABLESTACK Genie
ABLESTACK 클라우드 인프라 및 애플리케이션 배포 자동화 플랫폼

## Automation Controller 구성 정보
Docker 기반의 MiniKube를 사용하고 Single Node 아키텍처를 적용합니다.
- OS: CentOS 8.5 2111
- 요구 사양:
  - Automation Controller VM: 8Core 8G
  - Minikube Cluster: 4Core 6G


## Automation Controller 템플릿 구성 방법


### Automation Controller 템플릿 구성 준비
경로 "$ /genie/" 에 아래의 목록과 같이 설치에 필요한 파일들을 위치합니다.

```
$ ls -al

install_automation_controller_vm.sh         # Automation Controller 템플릿을 구성하기 위한 환경설정 쉘 스크립트
automation_controller_installation.yml      # Automation Controller 템플릿을 구성하기 위한 플레이북
check_port_forward.service                  # k8s 포트포워딩 상태 체크 서비스
check_port_forward.sh                       # k8s 포트포워딩 상태 체크 서비스의 쉘 스크립트
automation_controller_initialization.yml    # Automation Controller이 사용자에 의해 배포될 때 실행되는 플래이북 
```

### Automation Controller 템플릿 구성 쉘 스크립트 실행

```
$ sh ./install_automation_controller_vm.sh
```

### Automation Controller 템플릿 구성 확인
- mold에서 public ip를 할당합니다.
- 80/tcp 포트 허용합니다.
- http://<<public_ip>>:80 접속합니다.
- ID: genie / Password: password 로 로그인 합니다.


## Execution Environment(EE) 이미지 커스터마이징
다양한 플랫폼에서 일관성 있게 자동화 절차가 실행되도록 자동화 실행 환경(EE)을 사용합니다.
EE는 k8s환경에서 컨테이너 이미지로 구동되며 Ansible 플레이북을 실행하는 역할을 합니다. 
일관성있는 자동화 환경을 위해 미리 지정된 저장소의 EE이미지를 다운로드 받아 컨테이너 이미지를 실행하기 때문에
사전에 EE이미지의 커스터마이징이 필요합니다.

디폴트 상태의 EE이미지에서는 아래 리스트에 명시된 모듈, pip 패키지, 설정파일이 존재하지 않기 때문에 
플레이북을 사용하여 설치, 변경해야합니다.
- EE 이미지 변경 내용 예:
  - Asible 설정 변경
  - CS 모듈 설치 (Mold 컨트롤)
  - http.conf 변경

EE 커스터 마이징은 플레이북에 의해 공식 EE 컨테이너 이미지를 다운로드한 후 설정된 내용에 따라 변경된 다음, 자동으로 ABLECLOUD Docker Hub 저장소로 Push됩니다.
이미지의 tag는 latest로 저장되며 특정 버전으로 업로드할 때에는 "awx_ee_template.yml" 파일의 "docker_commit_tag" 변수를 변경합니다.

### Execution Environment(EE) 이미지 커스터마이징 준비
경로 "$ /genie/" 에 아래의 목록과 같이 설치에 필요한 파일들을 위치합니다.

```
$ ls -al

install_awx_ee.sh         # EE 컨테이너 이미지를 커스터마이징을 하기 위한 환경설정 쉘 스크립트
awx_ee_template.yml      # EE 컨테이너 이미지를 커스터마이징 실행하기 위한 플레이북
```

### Execution Environment(EE) 이미지 커스터마이징 쉘 스크립트 실행

```
$ sh ./install_awx_ee.sh
```