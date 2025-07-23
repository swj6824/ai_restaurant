from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {
    "apple": "사과입니다",
    "banana": "바나나입니다",
    "grape": "포도입니다",
}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        # 아이템이 없으면 404 에러를 발생시킵니다.
        # raise HTTPException(status_code=404, detail="Item not found")
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}
