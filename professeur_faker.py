import psycopg2
from psycopg2.extras import execute_batch
from faker import Faker
import random

# -----------------------------
# Database connection
# -----------------------------
DB_NAME = "mybd_kjf6"
DB_USER = "mybd_kjf6_user"
DB_PASSWORD = "XEEK9NpJmKG7mxsVdPhZ8QzLqZG2YsPO"
DB_HOST = "dpg-d5me6mm3jp1c73a26r4g-a.frankfurt-postgres.render.com"
DB_PORT = "5432"

fake = Faker(locale='fr_FR')

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

cur = conn.cursor()

# -----------------------------
# Get all departments
# -----------------------------
cur.execute("SELECT id, nom FROM departements;")
departments = cur.fetchall()

total = 0

try:
    for dept_id, dept_name in departments:
        batch = []
        num_profs = random.randint(25, 30)

        for _ in range(num_profs):
            batch.append((
                fake.last_name()[:100],
                fake.first_name()[:100],
                dept_id
            ))

        execute_batch(
            cur,
            """
            INSERT INTO professeurs (nom, prenom, departement_id)
            VALUES (%s, %s, %s)
            """,
            batch,
            page_size=200
        )

        conn.commit()
        total += len(batch)
        print(f"✔ {dept_name} → {len(batch)} professeurs ajoutés")

    print(f"\n✅ SUCCESS: {total} professeurs insérés")

except Exception as e:
    conn.rollback()
    print("❌ ERROR:", e)

finally:
    cur.close()
    conn.close()
