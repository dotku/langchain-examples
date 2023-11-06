import os
import pinecone
from dotenv import load_dotenv, find_dotenv
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from pinecone.core.client.exceptions import ApiException
from fastapi import APIRouter, FastAPI, HTTPException, Request, Body
from pydantic import BaseModel
from typing import Dict, Any, Optional, List


class Item(BaseModel):
    name: str
    description: Optional[str] = None


class Index(BaseModel):
    name: str
    dimension: int = 1536


class Doc(BaseModel):
    page_content: str
    metadata: Dict[str, Any]


class Embeddings(BaseModel):
    docs: List[Doc]
    index_name: str = "langchain-self-retriever-demo"


load_dotenv(find_dotenv(".env.local"))

llm = OpenAI()
chat_model = ChatOpenAI()
router = APIRouter()

pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"], environment=os.environ["PINECONE_ENV"]
)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@router.post("/items/")
async def create_item(item: Item):
    return {"message": f"{item.name} created"}


@app.get("/pinecone/indexs")
async def list_indexs():
    return pinecone.list_indexes()


@app.delete("/pinecone/indexs")
async def delete_index(index: Index):
    index_list = pinecone.list_indexes()
    if index.name not in index_list:
        raise HTTPException(
            status_code=404, detail=f"Index `{index.name}` does not exist"
        )
    pinecone.delete_index(index.name)
    index_list = pinecone.list_indexes()
    return index_list


@app.post("/pinecone/indexs")
async def create_index(index: Index):
    print("Creating index", index.name)
    index_list = pinecone.list_indexes()
    if index.name in index_list:
        raise HTTPException(
            status_code=409, detail=f"Index `{index.name}` already exists"
        )
    # pinecone.create_index(index.name, index.dimension)
    try:
        pinecone.create_index(index.name, index.dimension)
    except ApiException as e:
        print('except ApiException', e)
        raise HTTPException(
            status_code=e.status, detail=e.body
        )
    index_list = pinecone.list_indexes()
    return index_list


@app.post("/pinecone/embeddings")
async def create_embeddings(embeddings: Embeddings):
    return {"message": "embeddings created", "embeddings": embeddings}
    # embeddings = OpenAIEmbeddings()
    # vectorstore = Pinecone.from_documents(
    #     docs, embeddings, index_name
    # )

    # try:
    #     embeddings = llm.embed(document.text)
    # except Exception as e:
    #     print('except Exception', e)
    #     raise HTTPException(
    #         status_code=500, detail=e
    #     )
    # return embeddings

# embeddings = OpenAIEmbeddings()
# # pinecone.create_index("langchain-self-retriever-demo", dimension=1536)
# print(pinecone.list_indexes())

app.include_router(router)
