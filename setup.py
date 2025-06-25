#!/usr/bin/env python3
"""
프로젝트 초기화 스크립트
- 필요한 패키지 설치
- 환경 변수 설정 안내
- 개발 서버 실행 안내
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """requirements.txt에서 패키지 설치"""
    print("📦 패키지 설치 중...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 패키지 설치 완료!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 패키지 설치 실패: {e}")
        return False

def setup_env_file():
    """환경 변수 파일 설정 안내"""
    env_file = Path(".env")
    env_template = Path("env_template.txt")
    
    if not env_file.exists():
        if env_template.exists():
            print("\n🔧 환경 변수 설정:")
            print(f"1. {env_template} 파일을 .env로 복사하세요")
            print("2. .env 파일을 열어 실제 API 키로 수정하세요")
            print("   - GOOGLE_API_KEY: Gemini API 키")
            print("   - LANGSMITH_API_KEY: LangSmith API 키")
        else:
            print("⚠️ env_template.txt 파일이 없습니다")
    else:
        print("✅ .env 파일이 이미 존재합니다")

def show_run_instructions():
    """실행 방법 안내"""
    print("\n🚀 프로젝트 실행 방법:")
    print("\n1. 백엔드 서버 실행:")
    print("   cd backend")
    print("   python main.py")
    print("   또는")
    print("   uvicorn backend.main:app --reload")
    
    print("\n2. 프론트엔드 서버 실행 (새 터미널):")
    print("   cd frontend")
    print("   streamlit run app.py")
    
    print("\n3. 접속 URL:")
    print("   - 백엔드 API: http://localhost:8000")
    print("   - API 문서: http://localhost:8000/docs")
    print("   - 프론트엔드: http://localhost:8501")

def main():
    """메인 함수"""
    print("🏗️ 온라인 쇼핑 최저가 탐색 AI 에이전트 프로젝트 초기화")
    print("=" * 60)
    
    # 패키지 설치
    if install_requirements():
        # 환경 변수 설정 안내
        setup_env_file()
        
        # 실행 방법 안내
        show_run_instructions()
        
        print("\n🎉 프로젝트 초기화 완료!")
    else:
        print("\n❌ 프로젝트 초기화 실패")
        sys.exit(1)

if __name__ == "__main__":
    main() 