from sqlalchemy import text

def get_daily_statistics_query(group_by_field: str) -> str:
    """
    일별 통계를 피벗 형태로 조회하는 쿼리 생성
    
    Args:
        group_by_field: 그룹화할 필드명 (RegionName 또는 AlarmName)
    
    Returns:
        SQL 쿼리 문자열
    """
    day_columns = ",\n                ".join([
        f'COALESCE(SUM(CASE WHEN "Day" = {i} THEN "Count" END), 0) AS d{str(i).zfill(2)}'
        for i in range(1, 32)
    ])
    
    query = f"""
        SELECT DISTINCT
            "{group_by_field}",
            {day_columns},
            SUM("Count") AS total_count
        FROM "Statistics"
        WHERE "AlarmMonth" = :month
        GROUP BY "{group_by_field}"
        ORDER BY "{group_by_field}";
    """
    
    return text(query)

def get_alarm_statistics_query() -> text:
    """Slack 알람 통계 조회 쿼리"""
    return text("""
        SELECT "Alarm", "Region", "NodeName", count(*) as cnt
        FROM "SlackMessage"
        WHERE "NodeName" IS NOT NULL 
          AND "DateTime" >= :start 
          AND "DateTime" <= :end 
          AND "Status" = 'Firing'
        GROUP BY "Alarm", "Region", "NodeName"
        ORDER BY cnt DESC
    """)
