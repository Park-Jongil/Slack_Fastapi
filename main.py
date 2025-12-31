from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import text  # text 함수 임포트 필요
from typing import List
import uvicorn

# 1. DB 설정 (본인의 Postgres 정보로 수정: user:password@host:port/dbname)
DATABASE_URL = "postgresql://postgres:1331@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. DB 테이블 모델 정의
class TeamData(Base):
    __tablename__ = "team_data"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(String)  # team1, team2 등 트리 노드 ID와 매칭
    name = Column(String)
    status = Column(String)
    date = Column(String)

class SalesData(Base):
    __tablename__ = "sales_data"
    id = Column(Integer, primary_key=True)
    team_id = Column(String)  # team1, team2 등 트리 노드 ID와 매칭
    name = Column(String)
    status = Column(String)
    date = Column(String)


# 서버 시작 시 테이블 생성 (실제 운영 시에는 Alembic 권장)
Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 팀 ID와 모델 클래스를 매핑
TABLE_MAP = {
    "team1": TeamData,
    "team2": TeamData,
    "team3": SalesData,
    "team4": SalesData
}

@app.get("/", response_class=HTMLResponse)
async def read_main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/pages/{team_id}", response_class=HTMLResponse)
async def get_team_page(request: Request, team_id: str):
    # team_id에 따라 다른 html 파일을 반환 (파일이 없을 경우 대비 예외처리 필요)
    try:
        return templates.TemplateResponse(f"{team_id}.html", {"request": request, "team_id": team_id})
    except:
        return templates.TemplateResponse("default.html", {"request": request})

@app.get("/api/tree")
async def get_tree():
    # 이 부분은 고정된 트리 구조이거나, 필요시 다른 테이블에서 가져올 수 있습니다.
    return [
        {"id": "dept1", "text": "영업부", "children": [
            {"id": "team1", "text": "영업 1팀"},
            {"id": "team2", "text": "영업 2팀"}
        ]},
        {"id": "dept2", "text": "기술부", "children": [
            {"id": "team3", "text": "개발팀"},
            {"id": "team4", "text": "인프라팀"}
        ]}
    ]


@app.get("/api/data/{item_id}")
async def get_grid_data(item_id: str, db: Session = Depends(get_db)):
    # 매핑 테이블에서 모델을 가져오고, 없으면 기본 TeamData 사용
    model = TABLE_MAP.get(item_id, TeamData)
    
    results = db.query(model).filter(model.team_id == item_id).all()
#    results = db.query(model).all()
    return results

@app.get("/api/query/{item_id}")
async def get_query_data(item_id: str, month: str = "2025-12", db: Session = Depends(get_db)):
    # 1. 생 SQL 쿼리 작성 (파라미터는 :name 형식을 권장 - SQL 인젝션 방지)
    if (item_id=='slack1') :
        query = text(
            """
            SELECT DISTINCT
                "RegionName",
                COALESCE(SUM(CASE WHEN "Day" = 1 THEN "Count" END), 0) AS d01,
                COALESCE(SUM(CASE WHEN "Day" = 2 THEN "Count" END), 0) AS d02,
                COALESCE(SUM(CASE WHEN "Day" = 3 THEN "Count" END), 0) AS d03,
                COALESCE(SUM(CASE WHEN "Day" = 4 THEN "Count" END), 0) AS d04,
                COALESCE(SUM(CASE WHEN "Day" = 5 THEN "Count" END), 0) AS d05,
                COALESCE(SUM(CASE WHEN "Day" = 6 THEN "Count" END), 0) AS d06,
                COALESCE(SUM(CASE WHEN "Day" = 7 THEN "Count" END), 0) AS d07,
                COALESCE(SUM(CASE WHEN "Day" = 8 THEN "Count" END), 0) AS d08,
                COALESCE(SUM(CASE WHEN "Day" = 9 THEN "Count" END), 0) AS d09,
                COALESCE(SUM(CASE WHEN "Day" = 10 THEN "Count" END), 0) AS d10,
                COALESCE(SUM(CASE WHEN "Day" = 11 THEN "Count" END), 0) AS d11,
                COALESCE(SUM(CASE WHEN "Day" = 12 THEN "Count" END), 0) AS d12,
                COALESCE(SUM(CASE WHEN "Day" = 13 THEN "Count" END), 0) AS d13,
                COALESCE(SUM(CASE WHEN "Day" = 14 THEN "Count" END), 0) AS d14,
                COALESCE(SUM(CASE WHEN "Day" = 15 THEN "Count" END), 0) AS d15,
                COALESCE(SUM(CASE WHEN "Day" = 16 THEN "Count" END), 0) AS d16,
                COALESCE(SUM(CASE WHEN "Day" = 17 THEN "Count" END), 0) AS d17,
                COALESCE(SUM(CASE WHEN "Day" = 18 THEN "Count" END), 0) AS d18,
                COALESCE(SUM(CASE WHEN "Day" = 19 THEN "Count" END), 0) AS d19,
                COALESCE(SUM(CASE WHEN "Day" = 20 THEN "Count" END), 0) AS d20,
                COALESCE(SUM(CASE WHEN "Day" = 21 THEN "Count" END), 0) AS d21,
                COALESCE(SUM(CASE WHEN "Day" = 22 THEN "Count" END), 0) AS d22,
                COALESCE(SUM(CASE WHEN "Day" = 23 THEN "Count" END), 0) AS d23,
                COALESCE(SUM(CASE WHEN "Day" = 24 THEN "Count" END), 0) AS d24,
                COALESCE(SUM(CASE WHEN "Day" = 25 THEN "Count" END), 0) AS d25,
                COALESCE(SUM(CASE WHEN "Day" = 26 THEN "Count" END), 0) AS d26,
                COALESCE(SUM(CASE WHEN "Day" = 27 THEN "Count" END), 0) AS d27,
                COALESCE(SUM(CASE WHEN "Day" = 28 THEN "Count" END), 0) AS d28,
                COALESCE(SUM(CASE WHEN "Day" = 29 THEN "Count" END), 0) AS d29,
                COALESCE(SUM(CASE WHEN "Day" = 30 THEN "Count" END), 0) AS d30,
                COALESCE(SUM(CASE WHEN "Day" = 31 THEN "Count" END), 0) AS d31,
                SUM("Count") AS total_count
            FROM "Statistics"
            WHERE "AlarmMonth" = :month
            GROUP BY "RegionName"
            ORDER BY "RegionName";
        """
        )
    elif (item_id=='slack2') :
        query = text(
            """
            SELECT DISTINCT
                "AlarmName",
                COALESCE(SUM(CASE WHEN "Day" = 1 THEN "Count" END), 0) AS d01,
                COALESCE(SUM(CASE WHEN "Day" = 2 THEN "Count" END), 0) AS d02,
                COALESCE(SUM(CASE WHEN "Day" = 3 THEN "Count" END), 0) AS d03,
                COALESCE(SUM(CASE WHEN "Day" = 4 THEN "Count" END), 0) AS d04,
                COALESCE(SUM(CASE WHEN "Day" = 5 THEN "Count" END), 0) AS d05,
                COALESCE(SUM(CASE WHEN "Day" = 6 THEN "Count" END), 0) AS d06,
                COALESCE(SUM(CASE WHEN "Day" = 7 THEN "Count" END), 0) AS d07,
                COALESCE(SUM(CASE WHEN "Day" = 8 THEN "Count" END), 0) AS d08,
                COALESCE(SUM(CASE WHEN "Day" = 9 THEN "Count" END), 0) AS d09,
                COALESCE(SUM(CASE WHEN "Day" = 10 THEN "Count" END), 0) AS d10,
                COALESCE(SUM(CASE WHEN "Day" = 11 THEN "Count" END), 0) AS d11,
                COALESCE(SUM(CASE WHEN "Day" = 12 THEN "Count" END), 0) AS d12,
                COALESCE(SUM(CASE WHEN "Day" = 13 THEN "Count" END), 0) AS d13,
                COALESCE(SUM(CASE WHEN "Day" = 14 THEN "Count" END), 0) AS d14,
                COALESCE(SUM(CASE WHEN "Day" = 15 THEN "Count" END), 0) AS d15,
                COALESCE(SUM(CASE WHEN "Day" = 16 THEN "Count" END), 0) AS d16,
                COALESCE(SUM(CASE WHEN "Day" = 17 THEN "Count" END), 0) AS d17,
                COALESCE(SUM(CASE WHEN "Day" = 18 THEN "Count" END), 0) AS d18,
                COALESCE(SUM(CASE WHEN "Day" = 19 THEN "Count" END), 0) AS d19,
                COALESCE(SUM(CASE WHEN "Day" = 20 THEN "Count" END), 0) AS d20,
                COALESCE(SUM(CASE WHEN "Day" = 21 THEN "Count" END), 0) AS d21,
                COALESCE(SUM(CASE WHEN "Day" = 22 THEN "Count" END), 0) AS d22,
                COALESCE(SUM(CASE WHEN "Day" = 23 THEN "Count" END), 0) AS d23,
                COALESCE(SUM(CASE WHEN "Day" = 24 THEN "Count" END), 0) AS d24,
                COALESCE(SUM(CASE WHEN "Day" = 25 THEN "Count" END), 0) AS d25,
                COALESCE(SUM(CASE WHEN "Day" = 26 THEN "Count" END), 0) AS d26,
                COALESCE(SUM(CASE WHEN "Day" = 27 THEN "Count" END), 0) AS d27,
                COALESCE(SUM(CASE WHEN "Day" = 28 THEN "Count" END), 0) AS d28,
                COALESCE(SUM(CASE WHEN "Day" = 29 THEN "Count" END), 0) AS d29,
                COALESCE(SUM(CASE WHEN "Day" = 30 THEN "Count" END), 0) AS d30,
                COALESCE(SUM(CASE WHEN "Day" = 31 THEN "Count" END), 0) AS d31,
                SUM("Count") AS total_count
            FROM "Statistics"
            WHERE "AlarmMonth" = :month
            GROUP BY "AlarmName"
            ORDER BY "AlarmName";
        """
        )
    
    # 2. 쿼리 실행
    result = db.execute(query, {"month": month})
    return result.mappings().all() 

@app.get("/api/slack/alarms")
async def get_alarm_statistics(start: str, end: str, db: Session = Depends(get_db)):
    # 요청하신 쿼리 내용 적용 (PostgreSQL 문법에 맞게 큰따옴표 사용)
    query = text("""
        SELECT "Alarm", "Region", "NodeName", count(*) as cnt
        FROM "SlackMessage"
        WHERE "NodeName" IS NOT NULL 
          AND "DateTime" >= :start 
          AND "DateTime" <= :end 
          AND "Status" = 'Firing'
        GROUP BY "Alarm", "Region", "NodeName"
        ORDER BY cnt DESC
    """)
    
    result = db.execute(query, {"start": start, "end": end})
    return result.mappings().all()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


###
    query = text("""
        SELECT id, name, status, date 
        FROM team_data 
        WHERE team_id = :tid 
        ORDER BY date DESC
    """)
###