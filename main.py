from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
import uvicorn
import logging

from database import get_db, engine
from models import Base, TeamData, SalesData, SlackMessage
from schemas import TeamDataResponse, StatisticsResponse, AlarmStatisticsResponse
from queries import get_daily_statistics_query, get_alarm_statistics_query

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 서버 시작 시 테이블 생성 (실제 운영 시에는 Alembic 권장)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="운영서비스 현황 대시보드")
templates = Jinja2Templates(directory="templates")

# 팀 ID와 모델 클래스를 매핑
TABLE_MAP = {
    "team1": TeamData,
    "team2": TeamData,
    "team3": SalesData,
    "team4": SalesData
}

# 쿼리 타입 매핑
QUERY_TYPE_MAP = {
    "slack1": "RegionName",
    "slack2": "AlarmName"
}

@app.get("/", response_class=HTMLResponse)
async def read_main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/pages/{team_id}", response_class=HTMLResponse)
async def get_team_page(request: Request, team_id: str):
    """팀 ID에 따른 전용 페이지 반환"""
    try:
        return templates.TemplateResponse(
            f"{team_id}.html", 
            {"request": request, "team_id": team_id}
        )
    except Exception as e:
        logger.warning(f"Template not found for {team_id}: {e}")
        return templates.TemplateResponse(
            "default.html", 
            {"request": request, "team_id": team_id}
        )


@app.get("/api/data/{item_id}", response_model=List[TeamDataResponse])
async def get_grid_data(item_id: str, db: Session = Depends(get_db)):
    """팀 ID별 그리드 데이터 조회"""
    try:
        model = TABLE_MAP.get(item_id, TeamData)
        results = db.query(model).filter(model.team_id == item_id).all()
        return results
    except Exception as e:
        logger.error(f"Error fetching data for {item_id}: {e}")
        raise HTTPException(status_code=500, detail="데이터 조회 중 오류가 발생했습니다")

@app.get("/api/query/{item_id}", response_model=List[StatisticsResponse])
async def get_query_data(item_id: str, month: str = "2025-12", db: Session = Depends(get_db)):
    """일별 통계 데이터 조회 (피벗 형태)"""
    try:
        # 쿼리 타입 확인
        group_by_field = QUERY_TYPE_MAP.get(item_id)
        
        if not group_by_field:
            raise HTTPException(
                status_code=400, 
                detail=f"지원하지 않는 item_id입니다: {item_id}"
            )
        
        # 동적 쿼리 생성 및 실행
        query = get_daily_statistics_query(group_by_field)
        result = db.execute(query, {"month": month})
        
        return result.mappings().all()
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing query for {item_id}: {e}")
        raise HTTPException(status_code=500, detail="쿼리 실행 중 오류가 발생했습니다") 

@app.get("/api/slack/alarms", response_model=List[AlarmStatisticsResponse])
async def get_alarm_statistics(start: str, end: str, db: Session = Depends(get_db)):
    """Slack 알람 통계 조회 (기간별)"""
    try:
        logger.info(f"Fetching alarm statistics from {start} to {end}")
        query = get_alarm_statistics_query()
        result = db.execute(query, {"start": start, "end": end})
        data = result.mappings().all()
        logger.info(f"Found {len(data)} alarm records")
        return data
    except Exception as e:
        logger.error(f"Error fetching alarm statistics: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"알람 통계 조회 중 오류가 발생했습니다: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
