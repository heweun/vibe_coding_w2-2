import os
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from duckduckgo_search import DDGS

# 환경변수에서 API 키 가져오기
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# DuckDuckGo 검색 툴 정의
@tool
def search_web(query: str) -> str:
    """웹 검색을 수행하여 상품 정보를 찾습니다."""
    try:
        ddgs = DDGS()
        results = ddgs.text(query, max_results=5, region="ko-kr")
        
        if not results:
            return "검색 결과를 찾을 수 없습니다."
        
        # 검색 결과를 포맷팅
        formatted_results = []
        for i, result in enumerate(results[:5], 1):
            formatted_results.append(
                f"{i}. {result['title']}\n"
                f"   URL: {result['href']}\n"
                f"   내용: {result['body'][:200]}...\n"
            )
        
        return "\n".join(formatted_results)
    
    except Exception as e:
        return f"검색 중 오류가 발생했습니다: {str(e)}"

# Gemini LLM 모델 초기화
def create_llm():
    """Gemini LLM 모델을 생성합니다."""
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY 환경변수가 설정되지 않았습니다.")
    
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-preview-05-20",
        temperature=0.1,
        google_api_key=GOOGLE_API_KEY
    )

# React Agent 생성
def create_shopping_agent():
    """온라인 쇼핑 최저가 탐색 React Agent를 생성합니다."""
    llm = create_llm()
    tools = [search_web]
    
    system_prompt = """
    당신은 온라인 쇼핑 최저가 탐색 전문 AI 에이전트입니다.
    
    사용자가 원하는 상품에 대해:
    1. 웹 검색을 통해 관련 상품 정보를 수집합니다
    2. 여러 쇼핑몰의 가격을 비교합니다
    3. 최저가 정보와 구매 링크를 제공합니다
    4. 상품의 특징과 리뷰 정보도 함께 제공합니다
    
    항상 한국어로 친절하고 정확한 답변을 제공해주세요.
    검색 결과가 부족할 경우 추가 검색을 수행하여 더 나은 정보를 제공하세요.
    """
    
    agent = create_react_agent(
        llm,
        tools,
        prompt=system_prompt
    )
    
    return agent

# Agent 실행 함수
def run_shopping_agent(query: str) -> str:
    """쇼핑 에이전트를 실행하여 결과를 반환합니다."""
    try:
        agent = create_shopping_agent()
        
        # 에이전트 실행
        result = agent.invoke({
            "messages": [{"role": "user", "content": query}]
        })
        
        # 마지막 메시지에서 응답 추출
        if result and "messages" in result:
            last_message = result["messages"][-1]
            if hasattr(last_message, 'content'):
                return last_message.content
            else:
                return str(last_message)
        
        return "응답을 생성할 수 없습니다."
        
    except Exception as e:
        return f"에이전트 실행 중 오류가 발생했습니다: {str(e)}" 