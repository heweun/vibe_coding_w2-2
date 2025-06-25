"""
온라인 쇼핑 최저가 탐색 AI 에이전트 프론트엔드

Streamlit을 사용한 간단한 채팅 인터페이스
"""

import streamlit as st
import requests
import json
import time
from typing import Optional

# 페이지 설정
st.set_page_config(
    page_title="🛒 쇼핑 AI 에이전트",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 백엔드 API 설정
BACKEND_URL = "http://localhost:8000"

def call_chat_api(message: str, user_id: Optional[str] = None, session_id: Optional[str] = None) -> str:
    """백엔드 채팅 API 호출"""
    try:
        payload = {
            "message": message,
            "user_id": user_id,
            "session_id": session_id
        }
        
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "응답을 받을 수 없습니다.")
        else:
            return f"API 오류: {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        return f"연결 오류: {str(e)}"
    except Exception as e:
        return f"오류: {str(e)}"

def simulate_streaming_response(text: str):
    """스트리밍 응답 시뮬레이션 (사용자 경험 개선)"""
    if not text or not text.strip():
        yield text
        return
    
    words = text.split()
    if not words:
        yield text
        return
    
    for i, word in enumerate(words):
        yield " ".join(words[:i+1])
        time.sleep(0.02)  # 자연스러운 타이핑 효과

def check_backend_health() -> bool:
    """백엔드 상태 확인"""
    try:
        health_response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return health_response.status_code == 200
    except:
        return False

def main():
    """메인 애플리케이션"""
    
    # 헤더
    st.title("🛒 온라인 쇼핑 최저가 탐색 AI 에이전트")
    st.markdown("---")
    
    # 사이드바
    with st.sidebar:
        st.header("ℹ️ 사용 방법")
        st.markdown("""
        1. 찾고 싶은 상품을 입력하세요
        2. AI가 웹 검색을 통해 최저가 정보를 찾아드립니다
        3. 여러 쇼핑몰의 가격을 비교해 드립니다
        
        **예시:**
        - "아이폰 15 최저가 알려줘"
        - "삼성 갤럭시 S24 가격 비교"
        - "노트북 추천해줘"
        """)
        
        st.markdown("---")
        
        # 백엔드 상태 확인
        backend_status = check_backend_health()
        if backend_status:
            st.success("✅ 백엔드 연결됨")
        else:
            st.error("❌ 백엔드 연결 실패")
            st.warning("백엔드 서버가 실행 중인지 확인해주세요.")
        
        st.markdown("---")
        
        # 채팅 기록 초기화 버튼
        if st.button("🗑️ 채팅 기록 초기화", type="secondary"):
            st.session_state.messages = []
            st.rerun()
    
    # 메인 채팅 영역
    st.header("💬 AI 에이전트와 채팅")
    
    # 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # 환영 메시지 (첫 방문 시)
    if not st.session_state.messages:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown("""
            안녕하세요! 저는 온라인 쇼핑 최저가 탐색 AI 에이전트입니다. 🛒
            
            어떤 상품을 찾고 계신가요? 
            상품명을 입력해주시면 최저가 정보와 가격 비교를 도와드리겠습니다!
            """)
    
    # 채팅 메시지 표시
    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
    
    # 사용자 입력
    if prompt := st.chat_input("원하는 상품을 검색해보세요...", disabled=not backend_status):
        # 백엔드가 연결되지 않은 경우 처리
        if not backend_status:
            st.error("백엔드 서버에 연결할 수 없습니다. 서버 상태를 확인해주세요.")
            return
        
        # 사용자 메시지 추가 및 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        # AI 응답 생성
        with st.chat_message("assistant", avatar="🤖"):
            # 로딩 메시지
            message_placeholder = st.empty()
            message_placeholder.markdown("🔍 검색 중입니다...")
            
            # API 호출
            response = call_chat_api(prompt)
            
            # 스트리밍 효과로 응답 표시
            if response and "오류" not in response and "API 오류" not in response:
                message_placeholder.empty()
                full_response = ""
                response_placeholder = st.empty()
                
                # 스트리밍 시뮬레이션
                for partial_response in simulate_streaming_response(response):
                    full_response = partial_response
                    response_placeholder.markdown(full_response + "▋")
                    time.sleep(0.01)
                
                response_placeholder.markdown(full_response)
            else:
                # 오류 응답은 즉시 표시
                message_placeholder.markdown(response)
        
        # AI 응답 저장
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # 빈 채팅 상태에서 샘플 질문 제공
    if not st.session_state.messages:
        st.markdown("### 💡 이런 질문을 해보세요:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📱 아이폰 15 최저가", key="sample1"):
                # 샘플 질문을 입력으로 설정
                st.session_state['sample_query'] = "아이폰 15 최저가 알려줘"
                st.rerun()
        
        with col2:
            if st.button("💻 노트북 추천", key="sample2"):
                st.session_state['sample_query'] = "게이밍 노트북 추천해줘"
                st.rerun()
        
        with col3:
            if st.button("🎧 무선 이어폰", key="sample3"):
                st.session_state['sample_query'] = "에어팟 프로 최저가 찾아줘"
                st.rerun()
    
    # 샘플 쿼리 처리
    if 'sample_query' in st.session_state and backend_status:
        query = st.session_state['sample_query']
        del st.session_state['sample_query']
        
        # 사용자 메시지 추가 및 표시
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user", avatar="👤"):
            st.markdown(query)
        
        # AI 응답 생성
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("검색 중입니다..."):
                response = call_chat_api(query)
                st.markdown(response)
        
        # AI 응답 저장
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

if __name__ == "__main__":
    main() 