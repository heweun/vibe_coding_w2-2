from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

# 라우터 임포트
from backend.routers import chat

# 환경 변수 로드
load_dotenv()

app = FastAPI(
    title="온라인 쇼핑 최저가 탐색 AI 에이전트",
    description="LangGraph 기반 AI 에이전트를 활용한 온라인 쇼핑 최저가 탐색 자동화 시스템",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(chat.router)

@app.get("/")
async def root():
    """API 루트 엔드포인트"""
    return {
        "message": "온라인 쇼핑 최저가 탐색 AI 에이전트 API", 
        "version": "1.1.0",
        "status": "running",
        "features": ["GitHub Actions", "Auto PR/Issue Management"]
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}

if __name__ == "__main__":
    host = os.getenv("BACKEND_HOST", "localhost")
    port = int(os.getenv("BACKEND_PORT", 8000))
    
    uvicorn.run(app, host=host, port=port) 