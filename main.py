from fastapi import FastAPI, HTTPException, BackgroundTasks
from typing import List, Optional
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.concurrency import run_in_threadpool
import logging
import json

app = FastAPI(title='LLM API', summary='API для работы с LLM')

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)

def get_db_connection():
    return psycopg2.connect('postgres://postgres:Pfqrfjkz32@localhost:5432/LLM', cursor_factory=RealDictCursor)

class LlmItem(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: Optional[int] = None
    status: Optional[bool] = None

@app.get("/")
def read_root():
    return {"message": "API работает"}

@app.get("/llm_filtered")
def get_filtered_llm(
    price: Optional[int] = None, 
    vpn: Optional[bool] = None, 
    tag: Optional[str] = None, 
    description_contains: Optional[str] = None,
    page: int = 1, 
    limit: int = 10
):
    try:
        conditions = []
        if price is not None:
            conditions.append(f"tariff.price = %s")
        if vpn is not None:
            conditions.append(f"availability.status = %s")
        if tag is not None:
            conditions.append(f"tag.name = %s")
        if description_contains is not None:
            conditions.append(f"llm.description ILIKE %s")

        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        params = []
        if price is not None:
            params.append(price)
        if vpn is not None:
            params.append(vpn)
        if tag is not None:
            params.append(tag)
        if description_contains is not None:
            params.append(f"%{description_contains}%")

        query = f'''
            SELECT llm.id, llm.name, llm.description, tariff.price, availability.status
            FROM llm
            JOIN tariff ON llm.id = tariff.llm_id
            JOIN availability ON llm.id = availability.llm_id
            LEFT JOIN tarifftag ON tariff.id = tarifftag.tariff_id
            LEFT JOIN tag ON tarifftag.tag_id = tag.id
            WHERE {where_clause}
            ORDER BY llm.name ASC
            LIMIT %s OFFSET %s;
        '''

        params.extend([limit, (page - 1) * limit])

        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute(query, params)
            result = cur.fetchall()

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при загрузке данных: {e}")

async def get_data_from_pgsql(data):
    return {"data": "example"}

@app.get("/request")
async def request_db(data, background_tasks: BackgroundTasks):
    dict_of_result = await run_in_threadpool(get_data_from_pgsql, data)

    def chunk_emitter():
        chunk_size = 10
        result = json.dumps(dict_of_result)
        for i in range(0, len(result), chunk_size):
            yield result[i:i + chunk_size]

    headers = {'Content-Disposition': 'attachment; filename=data.json'}
    return StreamingResponse(chunk_emitter(), headers=headers, media_type='application/json')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)

@app.post("/llm_info")
def add_new_llm_items(items: List[LlmItem]):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            for item in items:
                query = '''
                    INSERT INTO llm (name, description)
                    VALUES (%s, %s)
                    ON CONFLICT (name) DO NOTHING;
                '''
                cur.execute(query, (item.name, item.description))
            conn.commit()
        return {"message": "Items added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при добавлении данных: {e}")
