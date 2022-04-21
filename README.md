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
임의의 경로 또는 "$ /genie/" 에 아래의 목록과 같이 설치에 필요한 파일들을 위치합니다.

```
$ ls -al

install_automation_controller_vm.sh         # Automation Controller 템플릿을 구성하기 위한 환경설정 쉘 스크립트
automation_controller_installation.yml      # Automation Controller 템플릿을 구성하기 위한 플레이북
check_port_forward.service                  # k8s 포트포워딩 상태 체크 서비스
check_port_forward.sh                       # k8s 포트포워딩 상태 체크 서비스의 쉘 스크립트
automation_controller_initialization.yml    # Automation Controller이 사용자에 의해 배포될 때 실행되는 플래이북 
```

### "automation_controller_installation.sh" 실행

```
$ sh ./install_automation_controller_vm.sh
```

### Automation Controller 템플릿 구성 확인
- mold에서 public ip를 할당합니다.
- 80/tcp 포트 허용합니다.
- http://<<public_ip>>:80 접속합니다.
- ID: genie / Password: password 로 로그인 합니다.
