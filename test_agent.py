"""
LangGraph Agent 테스트 스크립트

이 스크립트는 LangGraph React Agent가 제대로 작동하는지 테스트합니다.
실행하기 전에 GOOGLE_API_KEY 환경변수를 설정해야 합니다.
"""

import os
from dotenv import load_dotenv
from backend.agent import run_shopping_agent

def test_agent():
    """Agent 기본 기능 테스트"""
    # 환경변수 로드
    load_dotenv()
    
    # API 키 확인
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ GOOGLE_API_KEY 환경변수가 설정되지 않았습니다.")
        print("   .env 파일을 생성하고 GOOGLE_API_KEY를 설정해주세요.")
        return
    
    print("🤖 LangGraph Agent 테스트 시작...")
    print("=" * 50)
    
    # 테스트 쿼리들
    test_queries = [
        "아이폰 15 최저가 알려줘",
        "삼성 갤럭시 S24 가격 비교",
        "노트북 추천해줘"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 테스트 {i}: {query}")
        print("-" * 30)
        
        try:
            response = run_shopping_agent(query)
            print(f"✅ 응답: {response[:200]}...")
            
        except Exception as e:
            print(f"❌ 오류: {str(e)}")
    
    print("\n🎉 테스트 완료!")

if __name__ == "__main__":
    test_agent() 