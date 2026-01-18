import psycopg2

def get_connection():
    return psycopg2.connect(
         dbname="mybd_kjf6",
         user="mybd_kjf6_user",
         password="XEEK9NpJmKG7mxsVdPhZ8QzLqZG2YsPO",
         host="dpg-d5me6mm3jp1c73a26r4g-a.frankfurt-postgres.render.com",
         port="5432"
    )

 