##
Ruff와 mypy를 설치해줘


###
/plan 아래 두가지 api를 구현하고 싶어.
"""
## 1. 회식 이벤트 생성

- **POST /api/events**
  - 설명: 새로운 회식 이벤트를 생성합니다.
  - 요청 Body (JSON):
    ```json
    {
      "name": "2025년 7월 회식"
    }
    ```
  - 응답:
    - 201 Created
    - Body:
      ```json
      {
        "event_id": 1,
        "name": "2025년 7월 회식"
      }
      ```

## 2. 회식 이벤트 목록 조회

- **GET /api/events**
  - 설명: 생성된 모든 회식 이벤트를 조회합니다.
  - 응답:
    - 200 OK
    - Body:
      ```json
      [
        {"event_id": 1, "name": "2025년 7월 회식"},
        {"event_id": 2, "name": "2025년 8월 회식"}
      ]
      ```
"""