from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.event_router import router as event_router
from app import Base, engine

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="회식 메뉴 투표 API",
    description="익명의 참여자들이 특정 회식 이벤트에 대한 메뉴 후보를 제안하고, 투표하며, 그 결과를 확인할 수 있는 API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(event_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
