with psycopg2.connect() as conn:
 from fastapi import FastAPI
from typing import Union
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

def load_from_db_llm_without_vpn(name_of_table: str, name_of_table_availability: str):
    with psycopg2.connect('postgres://postgres:Pfqrfjkz32@localhost:5432/LLM', cursor_factory=RealDictCursor) as conn:
        cur = conn.cursor()

        query = f'SELECT llm.name ' \
                f'FROM {name_of_table}, {name_of_table_availability} ' \
                f'WHERE llm.id = availability.llm_id ' \
                f'AND availability.status = true ' \
                f'ORDER BY llm_id ASC;'
                #GROUP BY _
                #HAVING
        #print(query)
        cur.execute(query)
        return(cur.fetchall())

def load_from_db_llm_with_price_higher_than(price: int):
    with (psycopg2.connect('postgres://postgres:Pfqrfjkz32@localhost:5432/LLM', cursor_factory=RealDictCursor) as
          conn):
        cur = conn.cursor()

        query = f'SELECT llm.name, llm.description ' \
                f'FROM llm, tariff ' \
                f'WHERE llm.id = tariff.llm_id ' \
                f'AND tariff.price > {price} ' \
                f'ORDER BY llm.id ASC;'
        cur.execute(query)
        return(cur.fetchall())

def load_from_db_llm_with_price_and_vpn(price: int, vpn: str):
    with psycopg2.connect('postgres://postgres:Pfqrfjkz32@localhost:5432/LLM', cursor_factory=RealDictCursor) as conn:
        cur = conn.cursor()

        query = f'SELECT llm.name ' \
                f'FROM llm, tariff, availability ' \
                f'WHERE llm.id = tariff.llm_id ' \
                f'AND llm.id = availability.llm_id' \
                f'AND tariff.price = {price} ' \
                f'AND availability.status = {vpn}' \
                f'ORDER BY llm.name ASC;'
        cur.execute(query)
        return(cur.fetchall())

def load_from_db_llm_with_tag(tag: str):
    with psycopg2.connect('postgres://postgres:Pfqrfjkz32@localhost:5432/LLM', cursor_factory=RealDictCursor) as conn:
        cur = conn.cursor()

        query = f'SELECT llm.name ' \
                f'FROM llm, tariff, tarifftag, tag ' \
                f'WHERE llm.id = tariff.llm_id ' \
                f'AND tariff.id = tarifftag.tariff_id ' \
                f'AND tarifftag.tag_id = tag.id ' \
                f'AND tag.name = \'{tag}\' ' \
                f'ORDER BY llm.name ASC;'
        cur.execute(query)
        return(cur.fetchall())


app = FastAPI(title='LLM')


@app.get("/hello")
def get_hello_info(name: str, age: int= 10):
    # return {"name": name, "age": age, "Hello": "World"}
    return [name, age]

@app.get("/calculate")
def to_calculate(a: int, b: int):
    c = a + b
    return {"result": c}

@app.get("/llm with higher price than")
def get_llm(price: int):
    return [load_from_db_llm_with_price_higher_than(price)]

@app.get("/llm without VPN")
def get_llm(name_of_table: str, name_of_table_availability: str):
    return [load_from_db_llm_without_vpn(name_of_table, name_of_table_availability)]

@app.get("/llm with price and VPN")
def get_llm(price: int, vpn: str):
    return [load_from_db_llm_with_price_and_vpn(price, vpn)]

@app.get("/llm with tag")
def get_llm(tag: str):
    return [load_from_db_llm_with_tag(tag)]

class LlmItem(BaseModel):
    id: int
    name: str
    description: str = None

@app.post("/llm_info")
def add_new_llm_items(items: list[LlmItem]):
    with psycopg2.connect('postgres://postgres:Pfqrfjkz32@localhost:5432/LLM', cursor_factory=RealDictCursor) as conn:
        cur = conn.cursor()
        for item in items:
            query = f'INSERT INTO llm(id, name, description) VALUES (%s, %s, %s);'
            cur.execute(query, (item.id, item.name, item.description))
    return {"message": "added"}