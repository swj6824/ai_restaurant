from sqlalchemy.orm import Session  # DB 통역사

from . import models, schemas


# 여러명 조회
def get_users(db: Session, skip: int = 0, limit=100):
    return db.query(models.User).offset(skip).limit(limit).all()


# 특정 ID 조회
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# 이메일 기준으로 유저 조회
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# 유저 생성 API
def create_user(
    db: Session, user: schemas.UserCreate
):  # 유저 모델에서 객체를 생성 -> 비밀번호 해싱
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)  # DB에 추가
    db.commit()  # 실제 DB에 저장 반영
    db.refresh(db_user)  # 저장 후 db_user에 최신 정보 반영 (아이디 등 자동 생성 필드)
