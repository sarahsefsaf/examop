import psycopg2

# -----------------------------
# Database connection
# -----------------------------
DB_NAME = "mybd_kjf6"
DB_USER = "mybd_kjf6_user"
DB_PASSWORD = "XEEK9NpJmKG7mxsVdPhZ8QzLqZG2YsPO"
DB_HOST = "dpg-d5me6mm3jp1c73a26r4g-a.frankfurt-postgres.render.com"
DB_PORT = "5432"


conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
conn.autocommit = True
cur = conn.cursor()

# -----------------------------
# Optional: get department IDs to randomly assign rooms
# -----------------------------
cur.execute("SELECT id FROM departements;")
departments = [d[0] for d in cur.fetchall()]

# -----------------------------
# Insert 100 unique rooms
# -----------------------------
for i in range(1, 101):
    room_name = f"Salle {i}"
    capacite = 30 + (i % 20)  # just some variation: 30–49 seats
    dept_id = departments[i % len(departments)]  # distribute among departments
    cur.execute(
        "INSERT INTO salles (nom, capacite, departement_id) VALUES (%s, %s, %s)",
        (room_name, capacite, dept_id)
    )

cur.close()
conn.close()
print("✓ 100 salles inserted successfully!")
