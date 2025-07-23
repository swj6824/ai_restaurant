from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# 데이터 모델 정의
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


fake_items_db = []


# 전체 조회
@app.get("/items/")
async def read_item_list(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


# 생성
@app.post("/items/")
async def create_item(item: Item):
    fake_items_db.append(item)
    return item


# 개별 조회
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id <= 0 or item_id > len(fake_items_db):
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_items_db[item_id - 1]


# 수정
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id <= 0 or item_id > len(fake_items_db):
        raise HTTPException(status_code=404, detail="Item not found")
    fake_items_db[item_id - 1] = item
    return fake_items_db[item_id - 1]


# 삭제 둘 다 사용가능하니까 하나씩 주석문 처리해서 데이터 확인
@app.delete("/items/{item_id}")
async def delete_itme(item_id: int):
    if item_id <= 0 or item_id > len(fake_items_db):
        raise HTTPException(status_code=404, detail="Item not found")
    removed_item = fake_items_db.pop(
        item_id - 1
    )  # pop 쌓여있는거 중에서 맨 위에걸(맨마지막에 입력된 것) 꺼낸다고 생각하시면 됩니다. Stack 구조에서 나온 용어입니다.
    return {"deleted_item": removed_item}


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    fake_items_db.remove(fake_items_db[item_id - 1])
    return {item_id: item_id}


# uvicorn CRUD:app --reload
