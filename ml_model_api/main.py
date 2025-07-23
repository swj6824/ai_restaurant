from datetime import time

from fastapi import Cookie, FastAPI, Response

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI from WSL!"}


# 가상의 데이터베이스 (리스트로 구성)
fake_restaurant_db = [
    {
        "name": "김밥천국",
        "branch_name": "강남점",
        "description": "24시간 운영하는 분식 전문점",
        "address": "서울 강남구 테헤란로 123",
        "feature": "저렴한 가격, 빠른 제공",
        "is_closed": False,
        "latitude": 37.501274,
        "longitude": 127.039585,
        "phone": "02-1234-5678",
        "rating": 4.2,
        "rating_count": 120,
        "start_time": time(0, 0),
        "end_time": time(23, 59),
        "last_order_time": time(23, 30),
        "category": 1,
        "tags": ["분식", "가성비", "혼밥"],
    },
    {
        "name": "한솥도시락",
        "branch_name": "역삼점",
        "description": "도시락 전문 프랜차이즈",
        "address": "서울 강남구 역삼로 45",
        "feature": "다양한 메뉴, 포장 전문",
        "is_closed": False,
        "latitude": 37.499947,
        "longitude": 127.036102,
        "phone": "02-5678-1234",
        "rating": 4.0,
        "rating_count": 98,
        "start_time": time(9, 0),
        "end_time": time(21, 0),
        "last_order_time": time(20, 45),
        "category": 2,
        "tags": ["도시락", "배달", "프랜차이즈"],
    },
    {
        "name": "돈까스하우스",
        "branch_name": "선릉점",
        "description": "수제 돈까스를 판매하는 맛집",
        "address": "서울 강남구 선릉로 77",
        "feature": "바삭한 튀김, 일본식 정식",
        "is_closed": False,
        "latitude": 37.504456,
        "longitude": 127.048123,
        "phone": "02-3333-4444",
        "rating": 4.7,
        "rating_count": 250,
        "start_time": time(11, 0),
        "end_time": time(22, 0),
        "last_order_time": time(21, 30),
        "category": 3,
        "tags": ["돈까스", "수제", "일식"],
    },
]


# GET /restaurants/?skip=0&limit=2 → 처음 2개 반환
@app.get("/restaurants/")
def read_restaurants(
    skip: int = 0, limit: int = 10
):  # 전체가 100이라도 10개만 보여준다.
    return fake_restaurant_db[skip : skip + limit]  # 0: 1


@app.get("/items/")
async def read_items(ads_id: str | None = Cookie(default=None)):
    return {"ads_id": ads_id}


@app.get("/set-cookie/")
def set_cookie(response: Response):
    response.set_cookie(key="ads_id", value="abc123")
    return {"message": "ads_id 쿠키가 저장되었습니다!"}
