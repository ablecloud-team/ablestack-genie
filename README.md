# ABLESTACK Genie
ABLESTACK 클라우드 인프라 및 애플리케이션 배포 자동화 플랫폼

## Automation Controller 구성 정보
Docker 기반의 MiniKube를 사용하고 Single Node 아키텍처를 적용합니다.
- OS: CentOS 8.5 2111
- 요구 사양:
  - Automation Controller VM: 4Core 8G
  - Minikube Cluster: 2Core 3G

## ABLESTACK Genie 개발 구조
실행환경(Genie-EE) 도커 이미지와 Genie-Dashboard 도커이미지를 개발, 빌드한 후 이를 활용하여 Automation Controller 템플릿을 구성합니다.
![image](https://user-images.githubusercontent.com/34114265/183317067-fdc0b941-0c1c-4b57-b0de-bd2fc123c03f.png)

## Automation Controller 템플릿 구성 방법
Genie Shell을 활용하여 Genie Automation Controller 템플릿 구성을 쉽게 할 수 있습니다. <br>
<b>[Genie Shell 바로가기](./genie-shell/)</b>


