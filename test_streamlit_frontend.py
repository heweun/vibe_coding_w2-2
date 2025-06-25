"""
Streamlit 프론트엔드 테스트

TDD 방식으로 프론트엔드 기능을 검증합니다.
"""

import pytest
import requests
from unittest.mock import Mock, patch
import sys
import os
import time

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from frontend.app import call_chat_api, simulate_streaming_response, check_backend_health


class TestStreamlitFrontend:
    """Streamlit 프론트엔드 테스트 클래스"""

    def test_chat_api_call_success(self):
        """API 호출 성공 테스트"""
        # Mock 응답 설정
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "테스트 응답입니다"}
        
        with patch('requests.post', return_value=mock_response) as mock_post:
            result = call_chat_api("테스트 메시지")
            
            # 호출 검증
            mock_post.assert_called_once()
            args, kwargs = mock_post.call_args
            
            # URL 검증
            assert args[0] == "http://localhost:8000/chat"
            
            # JSON 페이로드 검증
            assert kwargs['json']['message'] == "테스트 메시지"
            assert 'timeout' in kwargs
            
            # 결과 검증
            assert result == "테스트 응답입니다"

    def test_chat_api_call_with_optional_params(self):
        """선택적 매개변수가 있는 API 호출 테스트"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "사용자 ID와 세션 ID가 포함된 응답"}
        
        with patch('requests.post', return_value=mock_response) as mock_post:
            result = call_chat_api(
                "테스트 메시지", 
                user_id="user123", 
                session_id="session456"
            )
            
            # 페이로드 검증
            args, kwargs = mock_post.call_args
            payload = kwargs['json']
            
            assert payload['message'] == "테스트 메시지"
            assert payload['user_id'] == "user123"
            assert payload['session_id'] == "session456"
            
            assert result == "사용자 ID와 세션 ID가 포함된 응답"

    def test_chat_api_call_http_error(self):
        """HTTP 오류 처리 테스트"""
        mock_response = Mock()
        mock_response.status_code = 500
        
        with patch('requests.post', return_value=mock_response):
            result = call_chat_api("테스트 메시지")
            
            assert result == "API 오류: 500"

    def test_chat_api_call_connection_error(self):
        """연결 오류 처리 테스트"""
        with patch('requests.post', side_effect=requests.exceptions.ConnectionError("연결 실패")):
            result = call_chat_api("테스트 메시지")
            
            assert "연결 오류:" in result
            assert "연결 실패" in result

    def test_chat_api_call_timeout_error(self):
        """타임아웃 오류 처리 테스트"""
        with patch('requests.post', side_effect=requests.exceptions.Timeout("요청 시간 초과")):
            result = call_chat_api("테스트 메시지")
            
            assert "연결 오류:" in result
            assert "요청 시간 초과" in result

    def test_chat_api_call_invalid_json_response(self):
        """잘못된 JSON 응답 처리 테스트"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}  # response 키가 없는 경우
        
        with patch('requests.post', return_value=mock_response):
            result = call_chat_api("테스트 메시지")
            
            assert result == "응답을 받을 수 없습니다."

    def test_chat_api_call_json_decode_error(self):
        """JSON 디코딩 오류 처리 테스트"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("JSON 디코딩 실패")
        
        with patch('requests.post', return_value=mock_response):
            result = call_chat_api("테스트 메시지")
            
            assert "오류:" in result

    @patch('frontend.app.BACKEND_URL', 'http://test-backend:9000')
    def test_backend_url_configuration(self):
        """백엔드 URL 설정 테스트"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "테스트"}
        
        with patch('requests.post', return_value=mock_response) as mock_post:
            call_chat_api("테스트")
            
            args, kwargs = mock_post.call_args
            assert args[0] == "http://test-backend:9000/chat"

    def test_empty_message_handling(self):
        """빈 메시지 처리 테스트"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "빈 메시지 응답"}
        
        with patch('requests.post', return_value=mock_response) as mock_post:
            result = call_chat_api("")
            
            args, kwargs = mock_post.call_args
            assert kwargs['json']['message'] == ""
            assert result == "빈 메시지 응답"

    def test_long_message_handling(self):
        """긴 메시지 처리 테스트"""
        long_message = "테스트 " * 1000  # 매우 긴 메시지
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "긴 메시지 처리됨"}
        
        with patch('requests.post', return_value=mock_response) as mock_post:
            result = call_chat_api(long_message)
            
            args, kwargs = mock_post.call_args
            assert kwargs['json']['message'] == long_message
            assert result == "긴 메시지 처리됨"


class TestStreamingFeatures:
    """스트리밍 기능 테스트"""

    def test_simulate_streaming_response_basic(self):
        """기본 스트리밍 응답 시뮬레이션 테스트"""
        test_text = "안녕하세요 테스트입니다"
        
        # 스트리밍 제너레이터 테스트
        responses = list(simulate_streaming_response(test_text))
        
        # 각 단계별로 단어가 누적되는지 확인
        expected_responses = [
            "안녕하세요",
            "안녕하세요 테스트입니다"
        ]
        
        assert len(responses) == 2
        assert responses == expected_responses

    def test_simulate_streaming_response_single_word(self):
        """단일 단어 스트리밍 테스트"""
        test_text = "안녕하세요"
        
        responses = list(simulate_streaming_response(test_text))
        
        assert len(responses) == 1
        assert responses[0] == "안녕하세요"

    def test_simulate_streaming_response_empty_text(self):
        """빈 텍스트 스트리밍 테스트"""
        test_text = ""
        
        responses = list(simulate_streaming_response(test_text))
        
        assert len(responses) == 1
        assert responses[0] == ""

    def test_simulate_streaming_response_whitespace_only(self):
        """공백만 있는 텍스트 스트리밍 테스트"""
        test_text = "   "
        
        responses = list(simulate_streaming_response(test_text))
        
        # 공백만 있는 경우 그대로 반환
        assert len(responses) == 1
        assert responses[0] == "   "

    @patch('time.sleep')
    def test_simulate_streaming_response_timing(self, mock_sleep):
        """스트리밍 응답의 타이밍 테스트"""
        test_text = "첫번째 두번째 세번째"
        
        list(simulate_streaming_response(test_text))
        
        # time.sleep이 호출되었는지 확인
        assert mock_sleep.call_count == 3
        # 각 호출이 0.02초로 설정되었는지 확인
        for call in mock_sleep.call_args_list:
            assert call[0][0] == 0.02


class TestBackendHealthCheck:
    """백엔드 상태 확인 테스트"""

    def test_check_backend_health_success(self):
        """백엔드 상태 확인 성공 테스트"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        with patch('requests.get', return_value=mock_response) as mock_get:
            result = check_backend_health()
            
            # 호출 검증
            mock_get.assert_called_once_with("http://localhost:8000/health", timeout=5)
            
            # 결과 검증
            assert result is True

    def test_check_backend_health_http_error(self):
        """백엔드 상태 확인 HTTP 오류 테스트"""
        mock_response = Mock()
        mock_response.status_code = 500
        
        with patch('requests.get', return_value=mock_response):
            result = check_backend_health()
            
            assert result is False

    def test_check_backend_health_connection_error(self):
        """백엔드 상태 확인 연결 오류 테스트"""
        with patch('requests.get', side_effect=requests.exceptions.ConnectionError("연결 실패")):
            result = check_backend_health()
            
            assert result is False

    def test_check_backend_health_timeout_error(self):
        """백엔드 상태 확인 타임아웃 오류 테스트"""
        with patch('requests.get', side_effect=requests.exceptions.Timeout("타임아웃")):
            result = check_backend_health()
            
            assert result is False

    def test_check_backend_health_generic_exception(self):
        """백엔드 상태 확인 일반적인 예외 테스트"""
        with patch('requests.get', side_effect=Exception("예상치 못한 오류")):
            result = check_backend_health()
            
            assert result is False

    @patch('frontend.app.BACKEND_URL', 'http://custom-backend:3000')
    def test_check_backend_health_custom_url(self):
        """커스텀 백엔드 URL 상태 확인 테스트"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        with patch('requests.get', return_value=mock_response) as mock_get:
            result = check_backend_health()
            
            mock_get.assert_called_once_with("http://custom-backend:3000/health", timeout=5)
            assert result is True


class TestStreamlitUIComponents:
    """Streamlit UI 컴포넌트 테스트"""

    def test_import_statements(self):
        """필요한 라이브러리 import 테스트"""
        try:
            import streamlit as st
            import requests
            import json
            import time
            from typing import Optional
            assert True
        except ImportError as e:
            pytest.fail(f"필요한 라이브러리를 import할 수 없습니다: {e}")

    def test_backend_url_constant(self):
        """백엔드 URL 상수 정의 테스트"""
        from frontend.app import BACKEND_URL
        assert BACKEND_URL == "http://localhost:8000"

    def test_chat_api_function_signature(self):
        """chat API 함수 시그니처 테스트"""
        import inspect
        from frontend.app import call_chat_api
        
        sig = inspect.signature(call_chat_api)
        params = list(sig.parameters.keys())
        
        assert 'message' in params
        assert 'user_id' in params
        assert 'session_id' in params
        
        # 선택적 매개변수 확인
        assert sig.parameters['user_id'].default is None
        assert sig.parameters['session_id'].default is None

    def test_streaming_function_signature(self):
        """스트리밍 함수 시그니처 테스트"""
        import inspect
        from frontend.app import simulate_streaming_response
        
        sig = inspect.signature(simulate_streaming_response)
        params = list(sig.parameters.keys())
        
        assert 'text' in params
        assert len(params) == 1

    def test_health_check_function_signature(self):
        """상태 확인 함수 시그니처 테스트"""
        import inspect
        from frontend.app import check_backend_health
        
        sig = inspect.signature(check_backend_health)
        params = list(sig.parameters.keys())
        
        # 매개변수가 없어야 함
        assert len(params) == 0
        
        # 반환 타입이 bool이어야 함
        assert sig.return_annotation == bool


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 