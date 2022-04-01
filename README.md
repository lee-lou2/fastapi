# API Server
> FastAPI 를 활용한 다양한 API

## Used To
- Framework : FastAPI
- Databases : MongoDB, Postgresql, SQLite, ElasticSearch
- Caches : Redis
- Container : Docker
- Deploy : AWS
- Monitoring : Flower

## Apps

> ### User
> - Oauth2 기반 사용자 관리
> - 클라이언트 키와 시크릿 키를 이용한 토큰 발급
> - 기능별 Permission 설정
> - 소셜 로그인 추가(구글)
> - 이메일 주소를 기반으로 로컬, 소셜 사용자 통합 관리

> ### Token
> - Access Token, Refresh Token 로 구분하여 발급
> - Token White List 를 이용해 신규 발급 Token 만 유효하도록 설정
> - Cache 에 White List 를 저장하여 빠른 검사

> ### Notice
> - Naver Cloud SENS 서비스를 이용한 SMS 발송
> - 구글 API를 이용한 Mail 발송 서비스
> - Slack 메신저 발송

> ### Celery
> - 비동기 테스크 관리
> - Flower 활용
> - background_task 와 함께 사용

> ### Scheduler
> - 스케쥴링 서비스 추가(APScheduler 사용)
> - Sqlite 메모리를 이용하여 스케쥴 보존

> ### Cafe24
> - 카페24 상품 조회
> - 토큰 발급 및 API 사용
> - 카페24 사이트간 상품 복사

> ### 카카오
> - 카카오 토큰 발급/재발급
> - 나에게 메시지 전송
> - 챗봇 메모 기능 추가
> - 카카오 AI 오픈 소스를 이용해 자동 답변 기능 추가
> - 스케쥴링 서비스와 연동하여 알람 기능 추가
> - 친구에게 메시지 보내기
> - 친구 목록 조회 등(준비중)

> ### 네이버
> - 네이버 검색 API 를 사용하여 데이터 수집
> - 스케쥴러를 이용하여 특정 키워드 데이터 자동 수집

> ### 검색 서비스
> - ElasticSearch 를 이용해 데이터 저장
> - 저장된 데이터 검색

> ### WebSocket
> - 기본적인 소켓 추가
> - 간단한 채팅 서비스

> ### GraphQL
> - Strawberry 라이브러리를 이용
> - SqlAlchemy 와 연동하여 데이터 조회

> ### Security
> - RSA 256 방식의 암호화
> - 공개키/비밀키를 이용

> ### ETC
> - 데이터베이스 데이터 암호화
> - docker-compose 를 통해 일괄 생성
> - Logger 추가(SQLite 에 저장 및 Middleware 에 등록)
> - FTP 에 이미지 등록


## Run

Git Clone :

```sh
git clone https://github.com/iamjmon/fastapi.git
```

환경 변수 생성 : `.env`, `.build 내 환경 설정 파일`

기본 명령어 :

```sh
uvicorn main:app --reload (--host, --port)
```

## Document

FastAPI 에서 기본으로 제공하는 `Swagger`를 이용하였습니다.

_API에 관한 기본적인 정보는 물론 직접 `테스트`도 가능합니다._

서버 실행 후 http://localhost/docs 에서 확인 가능합니다.

## Environment

프로그램 실행을 위해선 아래 버전 준수가 요구됩니다.

```sh
Python 3.8 이상
```

## Update

* 0.0.1
  * 최초 배포
  * JWT Authorization
  * Oauth2 Service
  * Set Base User
  * Url Router
  * Throttling(Limiter)
  * Database Setting
  * Add Apps
    * User : 사용자 관리
    * Token : 토큰 관리
    * Notice : 문자, 이메일, 슬랙 알림
    * ChatBot : 메모 및 AI 답변 봇 등
    * External : 카카오, 카페24 등의 서비스
    * Scheduler : 스케쥴링 서비스
  * Add Middlewares
  * Add Custom Exceptions
  * Set Backend Tasks
  * Encrypted Data
  * docker-compose 로 연동
  * Add APScheduler
  * Use ElasticSearch
  * Logger 등록
  * GraphQL 구현
  * WebSocket 추가

* 0.0.2
  * FTP에 이미지 업로드 기능 추가
  * 카카오 챗봇과 연동하여 챗봇에 이미지 업로드 시 실행
  * 구글 드라이브나 AWS S3 와 연동 예정

* 0.0.3
  * 카카오톡 친구에게 메시지 보내기 기능 추가
  * 현재는 개발 승인이 이뤄지지 않은 상태라 내 다른 계정으로만 보내기 구현

* 0.0.4
  * 챗봇 컨텐츠 종류에 따른 추가 처리
  * 이미지 등록시 자동 추가

* 0.0.5
  * 챗봇에 저장된 메모를 볼 수 있는 페이지 추가
  * 자신의 메모만 볼 수 있도록 설정
  * 챗봇을 통해 메모 링크를 생성할 수 있음
  * 생성한 링크는 3분만 접속 가능하도록 설정(캐시 사용)

* 0.0.6
  * 네이버 검색 API 사용하여 데이터 조회
  * 특정 키워드를 스케쥴러를 이용하여 자동 수집

* 0.0.7
  * RSA 256 암호화 모델링
  * 키 생성 및 복호화 코드 추가

* 0.0.8
  * 아파트 매매 정보 실시간 알람
  * 데이터베이스에 데이터 누적

## Contact

JAY | root@ja-y.com
