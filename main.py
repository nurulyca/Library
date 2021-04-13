from sqlalchemy import create_engine
from sqlalchemy.sql import text

def main():
    conn_str = 'postgresql://postgres:postgres@localhost:5432/schema'
    engine = create_engine(conn_str, echo=False)
    with engine.connect() as connection:
        qry = text("SELECT * FROM employee WHERE nik=:nik")
        # result = db.engine.execute(text)
        result = connection.execute(qry, nik='900080091')
        for row in result:
            print('name: \t\t', row['name'])
            print('start_year: \t', row['start_year'])
    # print('hello')

if __name__ == "__main__":
    main()
