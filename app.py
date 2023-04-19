from flask import Flask, send_file, after_this_request
from pandas import read_sql
from sqlalchemy import create_engine
import os

PORT = 5432
app = Flask(__name__)

@app.route('/download/<book_id>')
def show_customers(book_id):
    engine = create_engine(f"postgresql+psycopg2://:@localhost:{PORT}/biblabot")
    connection = engine.connect()
    read_sql(f"SELECT borrow_id, book_id, date_start, date_end FROM borrows", connection).\
        to_excel(f"book_{book_id}_info.xlsx")

    @after_this_request
    def remove_file(response):
        try:
            os.remove(f"book_{book_id}_info.xlsx")
        except Exception as error:
            app.logger.error("Error removing or closing downloaded file handle", error)
        return response
    return send_file(f"book_{book_id}_info.xlsx")


# if __name__ == '__main__':
#     app.run("0.0.0.0", port=8080)   