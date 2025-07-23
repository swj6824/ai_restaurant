from typing import Annotated

from fastapi import Depends


# 공통 쿼리 파라미터
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


# 의존성 타입으로 정의
CommonsDep = Annotated[dict, Depends(common_parameters)]
