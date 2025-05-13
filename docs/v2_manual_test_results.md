## Flow 2: Community Challenge Participation 🎯

Jeffery Bezos wants to kick off a friendly tagging contest around sad songs that feel empowering.

1. Jeffery calls `POST /challenges` with:
   - title: "Sad but Strong"
   - description: "Add to this challenge!"

2. His friend Elon participates by calling `POST /challenges/1/submissions` with:
   - tag_id: 4
   - tag_text: "So Sad!!!!"

3. Other users vote on Elon's tag via `POST /tags/upvote`.

4. At the end of the week, Jeffery calls `GET /challenges/weekly`  to see the weekly leaderboard, what’s trending, and how his challenge did.

---
## Testing Results 🔥
### 1. Create Challenge

```bash
curl -X 'POST' \
  'http://127.0.0.1:3000/challenges' \
  -H 'accept: application/json' \
  -H 'access_token: ILIKETOSING' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 6,
  "title": "Sad but Strong",
  "description": "Add to this challenge!"
}'
```

**Response Body:**

```
{
  "challenge_id": 1,
  "message": "Challenge created successfully"
}
```

---

### 2. Submit Challenge

```bash
curl -X 'POST' \
  'http://127.0.0.1:3000/challenges/1/submission' \
  -H 'accept: */*' \
  -H 'access_token: ILIKETOSING' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 7,
  "tag_id": 4
}'
```

**No Response Body** 


---
### 3. Create Upvote

```bash
curl -X 'POST' \
  'http://127.0.0.1:3000/tags/upvote' \
  -H 'accept: application/json' \
  -H 'access_token: ILIKETOSING' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 8,
  "tag_id": 4
}'
```

**Response Body:**

```
{
  "message": "Successfully upvoted!"
}
```

---
### 4. Weekly Leaderboard

```bash
curl -X 'POST' \
  'http://127.0.0.1:3000/challenges/weekly' \
  -H 'accept: application/json' \
  -H 'access_token: ILIKETOSING' \
  -d ''
```

**Response Body:**

```
[
  {
    "challenge_id": 1,
    "title": "Sad but Strong",
    "upvotes": 2
  }
]
```

---


## Flow 3: Linking with Other Users 👯

Tony Stark has been listening to a lot of music, but he's feeling a little lonely with all of the Avengers mad at him. He wants to be recommeneded other Sonic Link users who enjoy similar music.

1. Tony calls `POST /tags` with:
   - user_id: 4
   - song_id: "001pyq8FLNSL1C8orNLI0b"
   - tag_text: "Genius, Billionaire, Playboy, Philanthropist"

2. His friend Pepper Potts calls `POST /tags` with:
   - user_id: 5
   - song_id: "0017XiMkqbTfF2AUOzlhj6"
   - tag_text: "Smart, Rich, Playa, Humanitarian"

3. Pepper Potts also calls `POST /tags/upvote` on the tag that Tony made because she enjoys the song.

4. Tony then calls `GET /recommended` and is returned Pepper Potts' user_id, because she upvoted his tag and made her own tag with similar wording.

5. Tony can now call  `GET /users/:user_id/tags` with Pepper's user_id and see the music she's been enjoying and hopefully find new music.

---

## Testing Results 🔥
### 1. Create Tag

```bash
curl -X 'POST' \
  'http://127.0.0.1:3000/tags' \
  -H 'accept: application/json' \
  -H 'access_token: ILIKETOSING' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 4,
  "song_id": "001pyq8FLNSL1C8orNLI0b",
  "tag_text": "Genius, Billionaire, Playboy, Philanthropist"
}'
```

**Response Body:**

```
{
  "tag_id": 2,
  "message": "Tag created successfully"
}
```

---

### 2. Create Tag (Again)

```bash
curl -X 'POST' \
  'http://127.0.0.1:3000/tags' \
  -H 'accept: application/json' \
  -H 'access_token: ILIKETOSING' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 5,
  "song_id": "0017XiMkqbTfF2AUOzlhj6",
  "tag_text": "Genius, Playboy, Rich"
}'
```

**Response Body:**

```
{
  "tag_id": 3,
  "message": "Tag created successfully"
}
```

---

### 3. Create Upvote

```bash
curl -X 'POST' \
  'http://127.0.0.1:3000/tags/upvote' \
  -H 'accept: application/json' \
  -H 'access_token: ILIKETOSING' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 5,
  "tag_id": 2
}'
```

**Response Body:**

```
{
  "message": "Successfully upvoted!"
}
```

---

### 4. Recommended

```bash
curl -X 'GET' \
  'http://127.0.0.1:3000/recommended/4' \
  -H 'accept: application/json' \
  -H 'access_token: ILIKETOSING'
```

**Response Body:**

```
[
  {
    "user_id": 5,
    "similarity_score": 0.895
  }
]
```

---

### 5. Get Song Tags

```bash
curl -X 'GET' \
  'http://127.0.0.1:3000/tags/users/5/tags' \
  -H 'accept: application/json' \
  -H 'access_token: ILIKETOSING'
```

**Response Body:**

```
[
  {
    "tag_id": 3,
    "song_id": "0017XiMkqbTfF2AUOzlhj6",
    "tag_text": "Genius, Playboy, Rich",
    "upvotes": 0
  }
]
```

---
