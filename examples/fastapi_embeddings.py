from typing import List, Dict, Any
from fastapi import FastAPI, Body
from pydantic import BaseModel


class Doc(BaseModel):
    page_content: str
    metadata: Dict[str, Any]


app = FastAPI()


@app.post("/pinecone/embeddings")
async def create_embeddings(docs: List[Doc] = Body(...), index_name: str = "langchain-self-retriever-demo"):
    return {"message": "embeddings created"}
