from sqlalchemy import create_engine  # DB 연결을 위한 엔진
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # 연결공유 가능하게 설정
)

# DB 세션을 생성하는 클래스 생성
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)  # crud 생성기

# 모든 모델 클래스(테이블 객체)들은 Base를 상속받아서 정의한다.
Base = declarative_base()
