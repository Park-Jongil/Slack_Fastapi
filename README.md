# 운영서비스 현황 대시보드

FastAPI 기반의 운영 모니터링 대시보드 애플리케이션입니다.

## 기능

- Slack 알람 통계 (지역별/알람별)
- Rancher 클러스터 현황
- 월별 일일 통계 조회
- CSV 내보내기

## 설치 방법

1. 의존성 설치:
```bash
pip install -r requirements.txt
```

2. 환경 변수 설정:
`.env.example`을 `.env`로 복사하고 데이터베이스 정보를 입력하세요.

```bash
copy .env.example .env
```

3. 서버 실행:
```bash
python main.py
```

또는

```bash
uvicorn main:app --reload
```

## 프로젝트 구조

```
├── main.py              # FastAPI 애플리케이션 진입점
├── models.py            # SQLAlchemy 모델
├── schemas.py           # Pydantic 스키마
├── database.py          # 데이터베이스 연결 설정
├── config.py            # 환경 설정
├── queries.py           # SQL 쿼리 함수
├── templates/           # HTML 템플릿
│   ├── index.html
│   ├── slack1.html
│   ├── slack2.html
│   └── default.html
└── requirements.txt     # Python 의존성
```

## API 엔드포인트

- `GET /` - 메인 대시보드
- `GET /pages/{team_id}` - 팀별 페이지
- `GET /api/data/{item_id}` - 팀 데이터 조회
- `GET /api/query/{item_id}?month=YYYY-MM` - 월별 통계 조회
- `GET /api/slack/alarms?start=...&end=...` - Slack 알람 통계

## 기술 스택

- **Backend**: FastAPI, SQLAlchemy
- **Database**: PostgreSQL
- **Frontend**: Vanilla JS, AG-Grid
- **Validation**: Pydantic
