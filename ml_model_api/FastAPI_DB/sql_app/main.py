from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

app = FastAPI()

# 모델들을 DB에 생성
models.Base.metadata.create_all(bind=engine)


# 의존성 주입 함수 - 요청마다 DB 세션을 생성하고, 종료 시 닫는다.
def get_db():
    db = SessionLocal()  # DB 세션 객체 생성
    try:
        yield db  # 생성된 db를 FastAPI 내부에 전달함
        # return 뒤에는 실행이 안되지만
        # yield는 중간값을 넘겨주고 밑으로 실행합니다.
    finally:
        db.close()  # 요청 끝나면 자동으로 세션 닫음 Depends(get_db)로 쓰일 때 사용가능하다


# 라우터 및 사용자 생성 API
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)  # crud.py 나중에...
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# 사용자 목록조회 API
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_user(db, skip=skip, limit=limit)
    return users


# 특정 사용자 조회 API
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# 특정 사용자에게 아이템 추가 API
@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


# 전체 아이템 목록 조회 API
@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
