import psycopg2

def load_from_db_llm():
    with psycopg2.connect('postgres://postgres:Pfqrfjkz32@localhost:5432/LLM') as conn:
        cur = conn.cursor()

        query = f'SELECT * ' \
                f'FROM llm ' \
                f'ORDER BY llm.id ASC;'
                #GROUP BY _
                #HAVING
        #print(query)
        cur.execute(query)
        return cur.fetchall()


print(load_from_db_llm())