from config import *
from utils import read_html
from html_parser import parse_html
# from html_parser import parse_html
from pprint import pprint
from db import *
import time
def main():
    st=time.time()
    data=read_html(FILE_PATH)
    extracted_data=parse_html(data)
    con=make_connection()
    cursor=con.cursor()
    create_Table(cursor,TABLE_NAME)
    insert_into_db(extracted_data,cursor,con)
    con.commit()
    cursor.close()
    con.close()
    print(time.time()-st)
if __name__=="__main__":
    main()    


