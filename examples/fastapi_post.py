from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
from typing import Optional


class Item(BaseModel):
    name: str
    description: Optional[str] = None


class ResponseModel(BaseModel):
    message: str


app = FastAPI()
router = APIRouter()


@router.post("/items/", response_model=ResponseModel)
async def create_item(item: Item):
    return {"message": f"{item.name} created"}

app.include_router(router)
