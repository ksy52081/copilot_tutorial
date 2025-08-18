# Event Management System 재구축 계획서

## Overview

회식 이벤트 및 메뉴 투표 관리 FastAPI 백엔드 시스템을 구축합니다.

**시스템 목적:**
- 회식 이벤트 생성 및 조회
- 이벤트별 메뉴 후보 등록
- 메뉴에 대한 익명 투표
- 투표 결과 실시간 집계

**핵심 도메인 엔티티:**
1. **Event**: 회식 이벤트 (id, name)
2. **Menu**: 메뉴 후보 (id, event_id, name) 
3. **Vote**: 투표 (id, event_id, menu_id)

**기술 스택:**
- FastAPI (웹 프레임워크)
- SQLAlchemy (ORM) + SQLite (DB)
- Pydantic (데이터 검증)
- pytest (테스트)

## Requirements

### 1. API 엔드포인트 명세

**이벤트 관리:**
- `POST /api/events/` - 이벤트 생성 (Input: {name: str}, Output: {id: int, name: str})
- `GET /api/events/` - 모든 이벤트 조회 (Output: [{id: int, name: str}, ...])

**메뉴 관리:**
- `POST /api/events/{event_id}/menus` - 메뉴 추가 (Input: {name: str}, Output: {id: int, event_id: int, name: str})
- `GET /api/events/{event_id}/menus` - 이벤트 메뉴 목록 (Output: [{id: int, event_id: int, name: str}, ...])

**투표 시스템:**
- `POST /api/events/{event_id}/votes` - 투표하기 (Input: {menu_id: int}, Output: {id: int, event_id: int, menu_id: int})
- `GET /api/events/{event_id}/results` - 투표 결과 (Output: [{menu_id: int, menu_name: str, vote_count: int}, ...])

### 2. 데이터베이스 스키마

**events 테이블:**
```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL
);
```

**menus 테이블:**
```sql
CREATE TABLE menus (
    id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL,
    name VARCHAR NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events (id)
);
```

**votes 테이블:**
```sql
CREATE TABLE votes (
    id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL,
    menu_id INTEGER NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events (id),
    FOREIGN KEY (menu_id) REFERENCES menus (id)
);
```

### 3. 비즈니스 규칙

- 존재하지 않는 이벤트에 메뉴 추가 시 404 에러
- 존재하지 않는 이벤트에 투표 시 404 에러  
- 다른 이벤트의 메뉴에 투표 시 400 에러
- 투표 결과는 메뉴별 득표수로 집계
- 투표가 없는 메뉴도 결과에 포함 (득표수 0)

## Implementation Steps

### Phase 1: 프로젝트 초기화 및 환경 설정

**디렉토리 구조 생성:**
```
app/
├── __init__.py
├── main.py                 # FastAPI 애플리케이션
├── db.py                   # DB 연결 설정
├── api/                    # API 라우터
│   ├── __init__.py
│   ├── event_router.py
│   ├── menu_router.py
│   └── vote_router.py
├── models/                 # SQLAlchemy 모델
│   ├── __init__.py
│   ├── base.py
│   ├── event.py
│   ├── menu.py
│   └── vote.py
├── schemas/               # Pydantic 스키마
│   ├── __init__.py
│   ├── event.py
│   ├── menu.py
│   └── vote.py
├── service/               # 비즈니스 로직
│   ├── __init__.py
│   ├── event_service.py
│   ├── menu_service.py
│   └── vote_service.py
└── repository/            # 데이터 액세스
    ├── __init__.py
    ├── event_repository.py
    ├── menu_repository.py
    └── vote_repository.py

test/
├── conftest.py           # pytest 설정
├── test_event_api.py     # 단위 테스트
└── test_event_api_e2e.py # E2E 테스트
```

**requirements.txt 생성:**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
```

### Phase 2: 데이터베이스 설정 및 모델 구현

**DB 연결 설정 (app/db.py):**
- SQLite 데이터베이스 엔진 생성
- 세션 팩토리 설정
- `get_db()` 의존성 함수 구현
- `create_tables()` 테이블 생성 함수

**Base 모델 (app/models/base.py):**
- 공통 id 필드를 가진 추상 Base 클래스

**도메인 모델 구현:**
- Event 모델: name 필드, menus/votes 관계 설정
- Menu 모델: event_id(FK), name 필드, votes 관계 설정
- Vote 모델: event_id(FK), menu_id(FK) 필드
- 모든 관계에 cascade="all, delete-orphan" 적용

### Phase 3: Pydantic 스키마 정의

**각 도메인별 스키마 패턴:**
```python
# 기본 패턴
class EntityBase(BaseModel):
    # 공통 필드

class EntityCreate(EntityBase):
    # 생성용 스키마

class EntityResponse(EntityBase):
    id: int
    # 추가 필드
    
    class Config:
        from_attributes = True
```

**투표 결과용 특별 스키마:**
- VoteResult: menu_id, menu_name, vote_count 필드

### Phase 4: Repository 계층 구현

**각 Repository 공통 메서드:**
- `__init__(self, db: Session)`: DB 세션 주입
- `create()`: 엔티티 생성
- `get_by_id()`: ID로 조회
- `get_all()` 또는 `get_by_xxx()`: 목록 조회

**VoteRepository 특수 메서드:**
- `get_vote_results(event_id)`: LEFT JOIN으로 메뉴별 투표 집계
- COUNT, GROUP BY를 사용한 집계 쿼리 구현

### Phase 5: Service 계층 구현

**각 Service 공통 패턴:**
- Repository 의존성 주입
- 비즈니스 로직 검증 (존재하지 않는 리소스 체크)
- HTTPException을 통한 에러 처리
- Pydantic 모델 변환 (model_validate 사용)

**핵심 비즈니스 로직:**
- MenuService: 메뉴 생성 시 이벤트 존재 검증
- VoteService: 투표 시 이벤트 존재 + 메뉴-이벤트 연관성 검증

### Phase 6: API Router 구현

**Router 구현 패턴:**
- APIRouter 인스턴스 생성 (prefix, tags 설정)
- 각 엔드포인트마다 Service 의존성 주입
- Depends(get_db)로 DB 세션 주입
- response_model로 응답 스키마 지정

**URL 설계 원칙:**
- 계층적 리소스 구조 (/events/{id}/menus, /events/{id}/votes)
- RESTful HTTP 메서드 사용 (POST=생성, GET=조회)

### Phase 7: FastAPI 메인 애플리케이션

**main.py 구현 내용:**
- FastAPI 인스턴스 생성 (title, description, version 설정)
- CORS 미들웨어 추가 (모든 origin 허용)
- 모든 Router include
- startup 이벤트에서 create_tables() 호출
- 루트 엔드포인트 및 헬스체크 엔드포인트

### Phase 8: 테스트 구현

**conftest.py 설정:**
- 테스트용 SQLite 인메모리 DB 설정
- TestClient 픽스처 생성
- 각 테스트마다 DB 초기화/정리

**단위 테스트 (test_event_api.py):**
- 이벤트 생성, 조회 기능 테스트
- 존재하지 않는 리소스 접근 시 404 테스트

**E2E 테스트 (test_event_api_e2e.py):**
- 전체 투표 워크플로우 테스트 (이벤트 생성→메뉴 추가→투표→결과 조회)
- 잘못된 요청 시나리오 테스트

### Phase 9: 실행 및 검증

**개발 서버 실행:**
```bash
uvicorn app.main:app --reload
```

**API 문서 확인:**
- http://localhost:8000/docs (Swagger UI)
- 모든 엔드포인트 Try it out으로 테스트

**테스트 실행:**
```bash
pytest  # 모든 테스트 실행
```

**기능 검증 시나리오:**
1. 이벤트 생성 → 201 Created 응답 확인
2. 메뉴 2개 추가 → 메뉴 목록 조회로 확인
3. 각 메뉴에 투표 → 투표 결과 집계 확인
4. 존재하지 않는 리소스 접근 → 404 응답 확인

### 핵심 구현 포인트

**SQLAlchemy 관계 설정:**
- `relationship()` 사용 시 `back_populates` 양방향 설정
- CASCADE 삭제로 데이터 일관성 보장

**FastAPI 의존성 주입:**
- `Depends(get_db)`로 DB 세션 관리
- Service 계층에서 Repository 주입

**에러 처리 전략:**
- 404: 리소스 존재하지 않음
- 400: 잘못된 요청 (메뉴-이벤트 불일치)
- HTTPException 사용

**테스트 전략:**
- 각 테스트 독립성 보장 (DB 초기화)
- 해피 패스와 에러 시나리오 모두 테스트
- E2E 테스트로 전체 플로우 검증
