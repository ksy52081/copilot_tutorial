# 회식 이벤트 생성 및 목록 조회 API 구현 계획서

## 1. Overview

본 계획서는 FastAPI 기반 회식 메뉴 투표 시스템에 다음 두 가지 API를 구현하기 위한 상세 계획을 제시합니다:

1. **회식 이벤트 생성** (POST /api/events)
2. **회식 이벤트 목록 조회** (GET /api/events)

이 두 API는 회식 이벤트의 생성과 전체 이벤트 목록 조회를 담당하며, 익명 사용자를 위한 RESTful 엔드포인트로 동작합니다.

## 2. Requirements

- FastAPI 라우터에 두 엔드포인트 추가
- 요청/응답은 모두 JSON 형식
- 이벤트는 고유 식별자(`event_id`)와 이름(`name`)을 가짐
- 이벤트 생성 시 201 Created, 목록 조회 시 200 OK 반환
- DB에 이벤트 정보 저장 및 조회 (SQLite, SQLAlchemy 사용)
- Pydantic 스키마 정의 (요청/응답 DTO)
- 계층 구조(routers, service, repository, models, schemas) 준수
- 테스트 코드(TDD, pytest, TestClient) 작성
- 폴더별 `__init__.py` 파일 존재 확인
- 탭(tab) 기반 들여쓰기, 타입 힌트 적용

## 3. Implementation Steps

1. **DB 모델 정의**
   - `app/models/event.py`에 `Event` SQLAlchemy 모델 생성 (`event_id`, `name` 필드)
   - `app/models/__init__.py`에 import 추가

2. **Pydantic 스키마 정의**
   - `app/schemas/event.py`에 요청/응답용 스키마(`EventCreate`, `EventRead`) 작성
   - `app/schemas/__init__.py`에 import 추가

3. **Repository 계층 구현**
   - `app/repository/event_repository.py`에 이벤트 생성/조회 함수 구현
   - DB 세션을 받아 이벤트 추가 및 전체 조회 기능 제공
   - `app/repository/__init__.py`에 import 추가

4. **Service 계층 구현**
   - `app/service/event_service.py`에 비즈니스 로직 함수 구현 (repository 호출)
   - `app/service/__init__.py`에 import 추가

5. **Router 구현**
   - `app/api/event_router.py`에 FastAPI 라우터 작성
   - POST /api/events, GET /api/events 엔드포인트 구현
   - 요청/응답 스키마, 상태코드, 의존성 주입 적용
   - `app/api/__init__.py`에 import 및 router 등록
   - `app/main.py`에 router 포함

6. **테스트 코드 작성**
   - `test/` 디렉토리에 이벤트 생성/조회 통합 테스트 작성 (pytest, TestClient)
   - Given-When-Then 패턴, docstring, 다양한 유저 스토리 반영
   - `conftest.py`에 autouse fixture로 DB 초기화

7. **코딩 컨벤션 및 구조 점검**
   - 탭 들여쓰기, 타입 힌트, 계층별 역할 분리, `__init__.py` 확인

8. **테스트 실행 및 검증**
   - 모든 테스트가 통과하는지 확인

---

이 계획에 따라 단계별로 구현을 진행하면 요구하는 API를 안정적으로 완성할 수 있습니다.
