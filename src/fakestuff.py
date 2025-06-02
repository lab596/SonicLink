from faker import Faker
import random
import psycopg
from tqdm import tqdm

fake = Faker()
conn = psycopg.connect(
    dbname="mydatabase",
    user="myuser",
    password="mypassword",
    host="localhost",
    port=5431
)
cur = conn.cursor()

#UNCOMMENT THIS SECTION FIRST TO ADD 5K USERS

users = []
for _ in tqdm(range(5000), desc="Users"):
    users.append((fake.user_name(), fake.password()))

placeholders = ', '.join(['(%s, %s)'] * len(users))
flat_values = [val for pair in users for val in pair] 

query = f"""
    INSERT INTO account_users (username, password)
    VALUES {placeholders}
    RETURNING id
"""

cur.execute(query, flat_values)
user_ids = [row[0] for row in cur.fetchall()]
conn.commit() 
print(f"Inserted {len(user_ids)} users.")



# UNCOMMENT THIS PART SECOND TO ADD TAGS + UPVOTES
cur.execute("SELECT id FROM account_users")
user_ids = [row[0] for row in cur.fetchall()]

cur.execute("SELECT track_id FROM spotify_songs")
song_ids = [row[0] for row in cur.fetchall()]

print(f"Found {len(user_ids)} users and {len(song_ids)} songs.")

tags = [
    (random.choice(user_ids), random.choice(song_ids), fake.sentence(nb_words=random.randint(2, 5)))
    for _ in tqdm(range(500_000), desc="Tags")
]

batch_size = 5000
tag_ids = []
for i in tqdm(range(0, len(tags), batch_size), desc="Inserting Tags"):
    batch = tags[i:i + batch_size]
    placeholders = ", ".join(["(%s, %s, %s)"] * len(batch))
    flat_values = [val for triple in batch for val in triple]
    
    cur.execute(
        f"""
        INSERT INTO user_tags (user_id, track_id, tag_text)
        VALUES {placeholders}
        RETURNING id
        """,
        flat_values
    )
    tag_ids.extend([row[0] for row in cur.fetchall()])
    conn.commit()

print(f"Inserted {len(tag_ids)} tags.")

upvotes = set()
upvote_rows = []

while len(upvote_rows) < 1_000_000:
    user_id = random.choice(user_ids)
    tag_id = random.choice(tag_ids)
    key = (user_id, tag_id)
    if key in upvotes:
        continue
    upvotes.add(key)
    upvote_rows.append((tag_id, user_id))

for i in tqdm(range(0, len(upvote_rows), batch_size), desc="Inserting Upvotes"):
    batch = upvote_rows[i:i + batch_size]
    cur.executemany("""
        INSERT INTO user_tag_upvotes (tag_id, user_id)
        VALUES (%s, %s)
    """, batch)
    conn.commit()

print(f"Inserted {len(upvote_rows)} upvotes.")
conn.close()