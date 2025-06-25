# 🛒 온라인 쇼핑 최저가 탐색 AI 에이전트

LangGraph와 Google Gemini를 활용한 온라인 쇼핑 최저가 탐색 자동화 시스템입니다.

## 🎯 주요 기능

- **AI 기반 상품 검색**: DuckDuckGo 검색을 통한 상품 정보 수집
- **가격 비교**: 여러 쇼핑몰의 가격 비교 및 최저가 정보 제공
- **React Agent**: LangGraph 기반 ReAct 패턴으로 동작하는 AI 에이전트
- **실시간 채팅**: Streamlit 기반 채팅 인터페이스

## 🏗️ 기술 스택

### 백엔드
- **FastAPI**: RESTful API 서버
- **LangGraph**: AI 에이전트 프레임워크
- **Google Gemini**: LLM 모델 (gemini-2.5-flash-preview-05-20)
- **DuckDuckGo Search**: 웹 검색 도구

### 프론트엔드
- **Streamlit**: 웹 UI 프레임워크

## 📦 설치 및 실행

### 1. 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
```bash
# .env 파일 생성
cp env_template.txt .env

# .env 파일에서 다음 값들을 설정:
GOOGLE_API_KEY=your_google_api_key_here
```

### 3. 백엔드 서버 실행
```bash
python run_backend.py
```
- API 서버: http://localhost:8000
- API 문서: http://localhost:8000/docs

### 4. 프론트엔드 실행 (새 터미널)
```bash
python run_frontend.py
```
- 웹 앱: http://localhost:8501

## 🧪 테스트

### Agent 기능 테스트
```bash
python test_agent.py
```

### API 테스트
```bash
pytest test_fastapi_basic.py
```

## 💡 사용 예시

채팅창에 다음과 같이 입력해보세요:

- "아이폰 15 최저가 알려줘"
- "삼성 갤럭시 S24 가격 비교"
- "노트북 추천해줘"
- "애플워치 어디서 싸게 살 수 있어?"

## 🔧 개발

### 프로젝트 구조
```
week2-1/
├── backend/
│   ├── agent.py          # LangGraph Agent 구현
│   ├── main.py           # FastAPI 앱
│   ├── models.py         # Pydantic 모델
│   └── routers/
│       └── chat.py       # 채팅 API 라우터
├── frontend/
│   └── app.py            # Streamlit 앱
├── requirements.txt      # 패키지 의존성
└── README.md
```

### API 엔드포인트
- `POST /chat`: 채팅 메시지 처리
- `GET /health`: 헬스 체크
- `GET /`: API 정보

## 🔑 환경 변수

| 변수명 | 필수 | 설명 |
|--------|------|------|
| `GOOGLE_API_KEY` | ✅ | Google Gemini API 키 |
| `LANGCHAIN_TRACING_V2` | ❌ | LangSmith 추적 활성화 |
| `LANGCHAIN_API_KEY` | ❌ | LangSmith API 키 |
| `LANGCHAIN_PROJECT` | ❌ | LangSmith 프로젝트명 |

## 📝 라이선스

MIT License

## 🤝 기여

이슈나 PR을 통해 기여해주세요! 