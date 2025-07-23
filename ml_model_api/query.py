from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/search/")
async def search_items(
    q: Annotated[
        str, Query(min_length=3, max_length=50, description="검색 키워드")
    ] = ...,
    limit: Annotated[int, Query(ge=1, le=100, description="최대 결과 수 (1~100)")] = 5,
    offset: Annotated[int, Query(ge=0, description="몇번째 결과부터 시작할지")] = 0,
):
    dummy_data = [f"{q}_result_{i}" for i in range(1, 101)]

    return {
        "query": q,
        "limit": limit,
        "offset": offset,
        "results": dummy_data[offset : offset + limit],
        "message": "검색 성공",
    }
