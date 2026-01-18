import psycopg2
from psycopg2.extras import execute_batch
from faker import Faker

fake = Faker('fr_FR')

conn = psycopg2.connect(
    dbname="mybd_kjf6",
    user="mybd_kjf6_user",
    password="XEEK9NpJmKG7mxsVdPhZ8QzLqZG2YsPO",
    host="dpg-d5me6mm3jp1c73a26r4g-a.frankfurt-postgres.render.com",
    port="5432"
)

cur = conn.cursor()

# -------------------------
# Fetch departments
# -------------------------
cur.execute("SELECT id FROM departements ORDER BY id;")
departements = [d[0] for d in cur.fetchall()]

levels = ['L1', 'L2', 'L3', 'M1', 'M2']
students_per_department = 1857

base = students_per_department // len(levels)
rest = students_per_department % len(levels)

# -------------------------
# Reset table
# -------------------------
cur.execute("TRUNCATE TABLE etudiants RESTART IDENTITY CASCADE;")
conn.commit()

try:
    total = 0

    for dept_id in departements:
        batch = []

        for i, level in enumerate(levels):
            count = base + (1 if i < rest else 0)

            for _ in range(count):
                batch.append((
                    fake.last_name()[:100],
                    fake.first_name()[:100],
                    dept_id,
                    level
                ))

        execute_batch(
            cur,
            """
            INSERT INTO etudiants (nom, prenom, departement_id, niveau)
            VALUES (%s, %s, %s, %s)
            """,
            batch,
            page_size=500   # 🔥 très important
        )

        conn.commit()
        total += len(batch)
        print(f"✔ Department {dept_id} done → total = {total}")

    print(f"\n✅ SUCCESS: {total} students inserted")

except Exception as e:
    print("❌ ERROR:", e)

finally:
    cur.close()
    conn.close()
