from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List
from pydantic import BaseModel

app = FastAPI(title="LLM", summary="nhgghgh")


@app.get("/by_price")
def get_llm_by_price(price: int):
    query = (f'SELECT llm.id, llm.name, llm description FROM llm, tariff 'f'WHERE llm.id = tariff.llm_id AND tariff.price > {price};')
   
    with psycopg2.connect('postgres://postgres:Pfqrfjkz32@localhost:5432/LLM', cursor_factory=RealDictCursor) as conn:
        cur = conn.cursor()

        cur.execute(query)
        data = cur.fetchall()
    
    return data

class LlmItem(BaseModel):
    id: str
    name: str
    description: str = None

@app.post('/llm_info')
def add_new_llm_items(items: List[LlmItem]):
    with psycopg2.connect('postgres://postgres:Pfqrfjkz32@localhost:5432/LLM') as conn:
        cur = conn.cursor()
        for item in items:
            query = f"INSERT INTO llm(id, name, description) VALUES (%s, %s, %s);"
            cur.execute(query, (item.id, item.name, item.description))
    return{}