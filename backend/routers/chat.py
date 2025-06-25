from fastapi import APIRouter, HTTPException
from backend.models import ChatRequest, ChatResponse
from backend.agent import run_shopping_agent

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

@router.post("", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    채팅 API 엔드포인트
    
    사용자의 메시지를 받아서 LangGraph Agent를 통해 AI 응답을 반환합니다.
    """
    try:
        # LangGraph Agent를 통해 응답 생성
        response_message = run_shopping_agent(request.message)
        
        return ChatResponse(
            response=response_message,
            status="success",
            user_id=request.user_id,
            session_id=request.session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류가 발생했습니다: {str(e)}") 