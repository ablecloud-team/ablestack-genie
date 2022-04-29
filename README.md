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
경로 "$ /genie/" 에 아래의 목록과 같이 설치에 필요한 파일들을 위치합니다. (소스 위치: ablestack-genie/genie_shell/automation_controller_template/)

```
$ ls -al

install_automation_controller_template.sh   # Automation Controller 템플릿을 구성하기 위한 환경설정 쉘 스크립트
install_automation_controller_template.yml  # Automation Controller 템플릿을 구성하기 위한 플레이북
check_port_forward.service                  # k8s 포트포워딩 상태 체크 서비스
check_port_forward.sh                       # k8s 포트포워딩 상태 체크 서비스로 작동되는 쉘 스크립트
deploy_automation_controller.yml            # Automation Controller가 genie 사용자에 의해 배포될 때 cloud-init로 실행되는 플래이북 
```

### Automation Controller 템플릿 구성 쉘 스크립트 실행

```
$ sh ./install_automation_controller_template.sh
```

### Automation Controller 템플릿 구성 확인
- mold에서 public ip를 할당합니다.
- 80/tcp 포트 허용합니다.
- http://<<public_ip>>:80 접속합니다.
- ID: genie / Password: password 로 로그인 합니다.

<hr/>
<hr/>

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
경로 "$ /genie/" 에 아래의 목록과 같이 설치에 필요한 파일들을 위치합니다. (소스 위치: ablestack-genie/genie_shell/awx-ee/)

```
$ ls -al

customize_awx_ee.sh       # EE 컨테이너 이미지를 커스터마이징을 하기 위한 환경설정 쉘 스크립트
customize_awx_ee.yml      # EE 컨테이너 이미지를 커스터마이징 실행하기 위한 플레이북
```

### Execution Environment(EE) 이미지 커스터마이징 쉘 스크립트 실행

```
$ sh ./customize_awx_ee.sh
```

<hr/>
<hr/>

## AWX 개발환경 구성 및 컨테이너 이미지 생성
개발환경 플레이북을 실행하여 구성합니다.
개발환경 구성 이후 backend, ui 서버 동작은 개발자가 명령어를 통해 실행합니다.

### AWX 개발환경 구성 준비
- 경로 "$ /genie/" 에 아래의 목록과 같이 설치에 필요한 파일들을 위치합니다. (소스 위치: ablestack-genie/genie_shell/awx/)
- <span style="color:orange; font-weight:bold">'deploy_awx_devel_env.yml'를 편집하여 'Git repository', 'Docker 계정' 정보 등을 변경합니다.</span>

```
$ ls -al

deploy_awx_devel_env.sh   # Automation Controller AWX 개발환경을 구성하기 위한 환경설정 쉘 스크립트
deploy_awx_devel_env.yml  # Automation Controller AWX 개발환경을 구성하기 위한 플레이북
```

### AWX 개발환경 실행
- 개발환경 이미지 생성 확인
  ```
  $ docker images
  
  ------------------------------------------------------------------------------------------------------------------
  REPOSITORY                                   TAG                 IMAGE ID            CREATED             SIZE
  ansible/awx_devel                            latest              ba9ec3e8df74        26 minutes ago      1.42GB
  ------------------------------------------------------------------------------------------------------------------
  ```

- 개발환경 컨테이너 시작
  ```
  $ cd ./awx/           # deploy_awx_devel_env.yml에 의해 자동으로 다운로드된 awx 소스 폴더에 접근합니다.

  $ make docker-compose # docker-compose로 개발 환경 컨테이너들을 실행합니다.
  ```

- 개발환경 AWX 테스트용 계정 및 데이터 생성 (make docker-compose가 완료된 후 실행합니다.)
  ```
  $ docker exec -ti tools_awx_1 awx-manage createsuperuser
  $ docker exec tools_awx_1 awx-manage create_preload_data
  ```

- UI 서버 구성 및 실행
  ```
  $ npm --prefix=awx/ui install
  $ npm --prefix=awx/ui start
  ```

### AWX 개발 완료 후 빌드 및 패키징
- 클린 & 빌드
  ```
  $ docker exec tools_awx_1 make clean-ui ui-devel
  ```

- 컨테이너 이미지로 빌드 (이미지 이름 및 테그 확인 후 실행합니다.)
  ```
  $ ansible-playbook tools/ansible/build.yml \
    -e awx_image=stardom3645/awx-genie \
    -e awx_image_tag=latest -v
  ```

- 컨테이너 이미지 푸시 (저장소 확인 후 실행합니다.)
  ```
  $ docker push stardom3645/awx-genie:latest
  ```
