import csv
import psycopg2
import os

def load_to_db(path_to_file:str):
    with psycopg2.connect('postgres://postgres:Pfqrfjkz32@localhost:5432/LLM') as conn:
        cur=conn.cursor()

        with open(path_to_file,'r',encoding='utf-8') as file:
            reader=csv.reader(file)
            header=next(reader)
            fields=', '.join(header)
            table_name=path_to_file.split('.')[0].split('/')[-1].lower()

            values =', '.join(['%s' for _ in range(len(header))])

            query=(
                f"INSERT INTO {table_name.split(' - ')[-1]}({fields}) VALUES ({values})"
            )
            for item in reader:
                cur.execute(query,item)

def get_csv_file(path:str):
    for file_name in sorted(os.listdir(path)):
        if file_name.endswith('.csv'):
            path_to_file=f'{path}/{file_name}'
            print(path_to_file)
            load_to_db(path_to_file)

if __name__ == "__main__":
    path=r'C:\my files\python\database\d_b'
    get_csv_file(path)


# SELECT llm.name FROM llm, availability
# WHERE availability.status= false and availability.llm_id=llm.id