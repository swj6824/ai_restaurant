from fastapi import FastAPI, Form, HTTPException, Response, status
from fastapi.responses import JSONResponse
from passlib.context import CryptContext

app = FastAPI()  # FastAPI 인스턴스는 한 번만 선언합니다.

# 비밀번호 해싱 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 가상의 사용자 DB {실제 서비스에선 DB 연동 필요}
fake_users_db = {}


# [1] 회원가입 엔드포인트
@app.post("/signup")
def signup(
    username: str = Form(...), password: str = Form(...), response: Response = None
):

    # 1. 아이디 중복 확인
    if username in fake_users_db:
        raise HTTPException(status_code=400, detail="이미 존재하는 사용자입니다.")

    # 2. 비밀번호 해싱
    hashed_password = pwd_context.hash(password)

    # 3. 사용자 정보 저장
    fake_users_db[username] = {"username": username, "hashed_password": hashed_password}

    # 4. 토큰 생성 (예시)
    session_token = f"token-{username}"

    # 5. 쿠키에 토큰 심기
    response.set_cookie(
        key="sessionid", value=session_token, httponly=True, max_age=3600
    )

    # 6 응답 반환
    return {"message": f"{username}님, 회원가입이 완료되었습니다."}


# [2] API 정보 변환 (해더 포함)
@app.get("/api/info")
def get_api_info():
    content = {
        "service": "MyApp",
        "description": "This API provides service info.",
        "status": "running",
    }

    headers = {
        "X-API-Version": "1.0.0",  # 버전 정보
        "Content-Language": "en-US",  # 언어 설정
        "Cache-Control": "no-store",  # 캐시 금지
    }

    return JSONResponse(content=content, headers=headers)


# [3] 아이템 업서트 (삽입 또는 수정 + 상태코드 제어)
items_db = {"foo": {"name": "Fighters", "size": 6}}


@app.put("/items/{item_id}")
async def upsert_item(item_id: str, name: str, size: int, response: Response):
    if item_id in items_db:
        # 기존 아이템 수정
        items_db[item_id].update({"name": name, "size": size})
        return {"message": "Item updated", "item": items_db[item_id]}

    # 새 아이템 추가 → 상태코드 201로 변경
    new_item = {"name": name, "size": size}
    items_db[item_id] = new_item
    response.status_code = status.HTTP_201_CREATED
    return {"message": "Item created", "item": new_item}
