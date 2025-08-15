---
applyTo: '**'
---

# Swagger(OpenAPI) 접근 및 활용 지침

본 프로젝트는 FastAPI 기반으로, 자동으로 Swagger(OpenAPI) 문서가 생성됩니다. LLM이 API 문서화 및 테스트 기능을 제공할 때 아래 지침을 따르세요.

## 1. Swagger UI 접근

- FastAPI 서버 실행 후, 브라우저에서 아래 주소로 접속하면 Swagger UI를 사용할 수 있습니다.
  ```
  http://localhost:8000/docs
  ```
- OpenAPI 스키마(JSON)는 아래에서 확인할 수 있습니다.
  ```
  http://localhost:8000/openapi.json
  ```

## 2. Swagger UI 활용

- Swagger UI에서는 각 API 엔드포인트의 요청/응답 스펙, 파라미터, 예시 등을 확인할 수 있습니다.
- "Try it out" 기능을 통해 실제로 API를 호출하고 응답을 확인할 수 있습니다.
- 인증이 필요 없는 익명 API이므로 별도의 토큰 입력 없이 바로 테스트 가능합니다.

## 3. LLM 코드 생성 시 유의사항

- Swagger UI 접근 경로(`/docs`)와 OpenAPI 스키마 경로(`/openapi.json`)를 명확히 안내하세요.
- 문서화된 엔드포인트와 실제 API 스펙이 일치하는지 항상 확인하세요.
- API 명세 변경 시, Swagger 문서가 자동으로 갱신됨을 안내하세요.
- 예시 요청/응답은 실제 명세(api_spec.instructions.md)와 일치해야 합니다.
- Swagger UI를 통한 테스트 방법을 구체적으로 안내하세요.

## 4. 기타

- 모든 요청/응답은 JSON 형식입니다.
- Swagger 문서는 FastAPI가 자동으로 생성하므로 별도 설정이 필요 없습니다.
- 문서화된 엔드포인트를 기준으로 테스트 및 코드 생성을 진행하세요.

## Swagger / Manual Verification
- uvicorn으로 앱을 실행한 뒤 `/docs`가 열리는지 확인한다.
- 모든 엔드포인트의 request/response 예시가 표시되는지 확인한다.
- 최소 1개 happy-path를 Swagger "Try it out"으로 호출해 2xx를 확인한다.

## Quickstart
```bash
source .venv/bin/activate
uvicorn app.main:app --reload


API Docs
Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc