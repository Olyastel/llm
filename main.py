from fastapi import FastAPI
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

def get_db_connection():
    return psycopg2.connect('postgres://postgres:Pfqrfjkz32@localhost:5432/LLM', cursor_factory=RealDictCursor)

def load_from_db_llm_without_vpn(name_of_table: str, name_of_table_availability: str):
    with get_db_connection() as conn:
        cur = conn.cursor()
        query = f'''
            SELECT llm.name
            FROM {name_of_table} AS llm
            JOIN {name_of_table_availability} AS availability
            ON llm.id = availability.llm_id
            WHERE availability.status = TRUE
            ORDER BY llm_id ASC;
        '''
        cur.execute(query)
        return cur.fetchall()

def load_from_db_llm_with_price_higher_than(price: int):
    with get_db_connection() as conn:
        cur = conn.cursor()
        query = f'''
            SELECT llm.name, llm.description
            FROM llm
            JOIN tariff ON llm.id = tariff.llm_id
            WHERE tariff.price > {price}
            ORDER BY llm.id ASC;
        '''
        cur.execute(query)
        return cur.fetchall()

def load_from_db_llm_with_price_and_vpn(price: int, vpn: str):
    with get_db_connection() as conn:
        cur = conn.cursor()
        query = f'''
            SELECT llm.name
            FROM llm
            JOIN tariff ON llm.id = tariff.llm_id
            JOIN availability ON llm.id = availability.llm_id
            WHERE tariff.price = {price}
            AND availability.status = {vpn}
            ORDER BY llm.name ASC;
        '''
        cur.execute(query)
        return cur.fetchall()

def load_from_db_llm_with_tag(tag: str):
    with get_db_connection() as conn:
        cur = conn.cursor()
        query = f'''
            SELECT llm.name
            FROM llm
            JOIN tariff ON llm.id = tariff.llm_id
            JOIN tarifftag ON tariff.id = tarifftag.tariff_id
            JOIN tag ON tarifftag.tag_id = tag.id
            WHERE tag.name = '{tag}'
            ORDER BY llm.name ASC;
        '''
        cur.execute(query)
        return cur.fetchall()

app = FastAPI(title='LLM API', summary='API для работы с LLM')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)

class LlmItem(BaseModel):
    id: int
    name: str
    description: str = None

@app.get("/llm_by_price")
def get_llm_by_price(price: int):
    return load_from_db_llm_with_price_higher_than(price)

@app.get("/llm_without_vpn")
def get_llm_without_vpn(name_of_table: str, name_of_table_availability: str):
    return load_from_db_llm_without_vpn(name_of_table, name_of_table_availability)

@app.get("/llm_with_price_and_vpn")
def get_llm_with_price_and_vpn(price: int, vpn: str):
    return load_from_db_llm_with_price_and_vpn(price, vpn)

@app.get("/llm_with_tag")
def get_llm_with_tag(tag: str):
    return load_from_db_llm_with_tag(tag)

@app.post("/llm_info")
def add_new_llm_items(items: List[LlmItem]):
    with get_db_connection() as conn:
        cur = conn.cursor()
        for item in items:
            query = '''
                INSERT INTO llm (id, name, description)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING;  # Чтобы избежать дублирования по id
            '''
            cur.execute(query, (item.id, item.name, item.description))
        conn.commit()
    return {"message": "Items added successfully"}

