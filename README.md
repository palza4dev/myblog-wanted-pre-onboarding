# [문승준] 백엔드 프리온보딩 선발 과제

- [위코드 x 원티드] 백엔드 프리온보딩 선발 과제 제출용 Repository

- 코스 소개 [링크](https://www.wanted.co.kr/events/pre_onboarding_course_4?t=1635069780048)

- 과제 안내 [링크](https://wecode.notion.site/x-2f1edca34653419d8e109df1816197c2)

<br>

## 사용 기술

- Python 3.8.12
- Django 3.2.8
- Django-cors-headers 3.10.0
- PyJWT 2.3.0
- bcrypt 3.2.0

<br>

## 프로젝트 구조와 구현 방법

- myblog 프로젝트 개요

  - Python을 기반으로 Django 프레임워크를 활용한 게시글 CRUD 기능 REST API 개발
  - 유저 생성과 인증, 인가 기능 개발

  

- DB와 모델링

  - sqlite3 사용
  - 유저 정보는 이름, 닉네임, 이메일, 패스워드 관리
  - 게시글 정보는 타이틀과 내용을 관리하고 작성한 유저를 참조하는 외래키 설정

  

- core app

  - 모든 데이터의 생성과 수정 이력관리를 위한 추상화 모델 TimeStampModel class 작성

    

- users app

  - 유저 회원가입을 위한 SignUpView class 작성 (bcrypt로 비밀번호 암호화)

  - 유저 로그인을 위한 LogInView class 작성 (JWT 토큰 생성)

  - 유저 인가를 위한 login_decorator를 utils.py에 작성

    

- posts app 

  - 글 작성, 글 목록 조회를 위한 PostView 작성
  - 글 내용 확인, 수정, 삭제를 위한 PostDetailView 작성



- Integration Test
  - Postman과 Httpie 활용
  - Postman Document [링크](https://web.postman.co/documentation/17676214-e908a12e-1170-49b0-be36-a9f8ce0caf10/publish?workspaceId=d421537f-5bf1-4172-a044-aea332407b9a)

<br>

## API 명세 - 엔드포인트와 호출&응답 예시

> 에러 메시지는 JSON Decode Error, Key Error, Value Error 등 명시된 것들을 제외하고 작성함



- ### 회원가입

  ```bash
  POST http://localhost:8000/users/signup
  -d {
      "name" : "아이유",
      "nickname" : "helloiuiu",
      "email": "iuiuiu@gmail.com",
      "password": "m111111!!"
  }
  
  => {
      "message": "SUCCESS"
  }
  ```
   - 에러 메시지
 
  ```bash
  중복된 닉네임 입력시
  => { "message": "NICKNAME_ALREADY_EXIST"}
  
  중복된 이메일 입력시
  => { "message": "EMAIL_ALREADY_EXIST"}
  
  이메일 양식 오류
  => { "message": "INVALID_EMAIL"}
  
  비밀번호 양식 오류
  => { "message": "INVALID_PASSWORD"}
  ```

  

- ### 로그인

  ```bash
  POST http://localhost:8000/users/login
  -d {
      "email": "iuiuiu@gmail.com",
      "password": "m111111!!"
  }
  
  => {
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.t0Hb9baTacCOS6849f6SmI1GShuLcsRQJqYTudHg9-k"
  }
  ```

  - 에러 메시지

  ```bash
  이메일 정보가 틀렸을때
  => { "message": "INVALID_EMAIL"}
  
  패스워드가 틀렸을때
  => { "message": "INVALID_USER_PASSWORD"}
  
  ```

  

- ### 게시글 작성

  ```bash
  POST http://localhost:8000/posts
  -h "Authorization: <access_token>"
  -d {
      "title" : "테스트 제목",
      "content" : "테스트 본문......"
  }
  
  => {
      "data": {
          "title": "테스트 제목",
          "content": "테스트 본문......"
      }
  }
  ```



- ### 게시글 목록 조회

  ```bash
  GET http://localhost:8000/posts?limit=3&offset=0
  
  => {
      "count": 3,
      "data": [
          {
              "post_id": 1,
              "user": "아이유",
              "title": "나의 첫번째 일기",
              "created_at": "2021-10-24T23:17:52.962",
              "updated_at": "2021-10-24T23:17:52.962"
          },
          {
              "post_id": 2,
              "user": "정우성",
              "title": "두번째 테스트 일기",
              "created_at": "2021-10-24T23:18:58.845",
              "updated_at": "2021-10-24T23:18:58.845"
          },
          {
              "post_id": 3,
              "user": "가물치",
              "title": "테스트 세번째 일기",
              "created_at": "2021-10-24T23:20:40.558",
              "updated_at": "2021-10-24T23:20:40.559"
          }
      ]
  }
  ```

  - 에러 메시지

  ```bash
  limit 값이 10을 넘으면
  => {"message" : "TOO_MUCH_LIMIT"}
  ```



- ### 게시글 내용 확인

  ```bash
  GET http://localhost:8000/posts/<int:post_id>
  -h "Authorization: <access_token>"
  
  => {
      "data": {
          "post_id": 2,
          "user": "정우성",
          "title": "두번째 테스트 일기",
          "content": "서기 4333년이 되고....",
          "created_at": "2021-10-24T23:18:58.845",
          "updated_at": "2021-10-24T23:18:58.845"
      }
  }
  ```

  - 에러 메시지

  ```bash
  해당 post가 존재하지 않을 때
  => {"message" : "POST_NOT_FOUND"}
  ```



- ### 게시글 내용 수정

  ```bash
  PATCH http://localhost:8000/posts/<int:post_id>
  -h "Authorization: <access_token>"
  -d {
      "title" : "제목만 수정 확인완료",
      "content" : "본문 수정 완료 확인"
  }
  
  => {
      "result": "UPDATED"
  }
  ```

  - 에러 메시지

  ```bash
  해당 유저가 작성한 게시글이 아닐때
  => {"message" : "INVALID_POST_ID"}
  ```



- ### 게시글 삭제

  ```bash
  DELETE http://localhost:8000/posts/<int:post_id>
  -h "Authorization: <access_token>"
  
  => {
      "message": "post_id <int:post_id> is DELETED"
  }
  ```

  - 에러 메시지

  ```bash
  해당 유저가 작성한 게시글이 아닐때
  => {"message" : "INVALID_POST_ID"}
  ```
