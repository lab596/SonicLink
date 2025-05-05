## Flow 1: Tag Creation and Upvote Interaction 🔥

Rohan discovers a new Japenese bop track that reminds him of Tokyo Drift. He decides to tag the song.

1. Rohan calls `GET /account` since he doesnt have an account yet. This generates his user id.

2. Rohan calls `POST /tags` with:
   - user_id: 1
   - song_id: "spotify:track:abc123"
   - tag_text: "drifting into the lead"

3. His friend Lebron sees the tag and resonates with it. He calls `POST /tags/upvote` with his user_id.

4. Rohan checks how well his tags are doing by calling `GET /users/1/tags`.

---
## Testing Results 🔥
1. curl -X 'POST' \
  'http://127.0.0.1:3000/account/new' \
  -H 'accept: application/json' \
  -H 'access_token: ILIKETOSING' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "Rohan",
  "password": "mypassword"
  }'
  - Response Body:
    {
    "id": 1
    }
2. curl -X 'POST' \
  'http://127.0.0.1:3000/tags' \
  -H 'accept: application/json' \
  -H 'access_token: ILIKETOSING' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 1,
  "song_id": "7yesZrAOvMYmVVkEzSF13g",
  "tag_text": "drifting into the lead"
  }'
  - Response Body:
    {
    "tag_id": 2,
    "message": "Tag created successfully"
    }
3. curl -X 'POST' \
  'http://127.0.0.1:3000/tags/upvote' \
  -H 'accept: application/json' \
  -H 'access_token: ILIKETOSING' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 3,
  "tag_id": 2

  }'
  - Response Body:
    {
    "message": "Successfully upvoted!"
    }
- finish when kip adds `GET /users/1/tags
  ---
