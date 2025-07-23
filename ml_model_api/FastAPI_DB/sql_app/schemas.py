from pydantic import BaseModel


class ItemBase(BaseModel):  # 공통요소
    """"""


class ItemCreate(ItemBase):
    """"""


class Item(ItemBase):  # 응답용
    """"""


class UserBase(BaseModel):  # 공통요소
    email: str


class UserCreate(UserBase):  # 응답 요청용(write)
    password: str


class User(UserBase):  # 응답용(read)
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
