import pytest
import httpx
from fastapi.testclient import TestClient
from backend.main import app

# 테스트 클라이언트 설정
client = TestClient(app)

class TestHealthCheck:
    """헬스체크 엔드포인트 테스트"""
    
    def test_health_endpoint_exists(self):
        """헬스체크 엔드포인트가 존재하는지 테스트"""
        response = client.get("/health")
        assert response.status_code == 200
        
    def test_health_endpoint_response_format(self):
        """헬스체크 엔드포인트 응답 형식 테스트"""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

class TestChatAPI:
    """채팅 API 엔드포인트 테스트"""
    
    def test_chat_endpoint_exists(self):
        """채팅 엔드포인트가 존재하는지 테스트"""
        response = client.post("/chat", json={"message": "test"})
        assert response.status_code == 200
        
    def test_chat_endpoint_post_method(self):
        """채팅 엔드포인트가 POST 메서드를 지원하는지 테스트"""
        response = client.post("/chat", json={"message": "Hello"})
        assert response.status_code == 200
        
        # GET 요청은 허용되지 않아야 함
        get_response = client.get("/chat")
        assert get_response.status_code == 405  # Method Not Allowed
        
    def test_chat_request_validation(self):
        """채팅 요청 데이터 검증 테스트"""
        # 올바른 요청
        valid_request = {"message": "안녕하세요"}
        response = client.post("/chat", json=valid_request)
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "status" in data
        assert data["status"] == "success"
        
        # 잘못된 요청 (message 없음)
        invalid_request = {"text": "잘못된 키"}
        invalid_response = client.post("/chat", json=invalid_request)
        assert invalid_response.status_code == 422  # Unprocessable Entity

class TestAPIStructure:
    """API 구조 테스트"""
    
    def test_fastapi_app_creation(self):
        """FastAPI 앱이 올바르게 생성되었는지 테스트"""
        from backend.main import app
        assert app.title == "온라인 쇼핑 최저가 탐색 AI 에이전트"
        assert app.version == "1.0.0"
        
    def test_cors_middleware_configured(self):
        """CORS 미들웨어가 설정되었는지 테스트"""
        # CORS 헤더가 포함된 실제 요청으로 테스트
        response = client.get("/health", headers={"Origin": "http://localhost:3000"})
        assert response.status_code == 200
        # CORS 헤더가 응답에 포함되어 있는지 확인
        assert "access-control-allow-origin" in response.headers
        
    def test_root_endpoint(self):
        """루트 엔드포인트 테스트"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "status" in data 