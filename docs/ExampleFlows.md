# SonicLink Example Flows

---

## Flow 1: Tag Creation and Upvote Interaction 🔥

Rohan discovers a new Japenese bop track that reminds him of Tokyo Drift. He decides to tag the song.

1. Rohan calls `GET /account` since he doesnt have an account yet. This generates his user id.

2. Rohan calls `POST /tags` with:
   - user_id: 1
   - song_id: "spotify:track:abc123"
   - tag_text: "drifting into the lead"

3. His friend Lebron sees the tag and resonates with it. He calls `POST /tags/456/upvote` with his user_id.

4. Rohan checks how well his tags are doing by calling `GET /users/1/tags`.

---

## Flow 2: Community Challenge Participation 🎯

Jeffery Bezos wants to kick off a friendly tagging contest around sad songs that feel empowering.

1. Leo calls `POST /challenges` with:
   - title: "Sad but Strong"
   - song_id: "spotify:track:def789"

2. His friend Elon participates by calling `POST /challenges/789/submissions` with:
   - tag_text: "cry then conquer"

3. Other users vote on Elon's tag via `POST /tags/987/upvote`.

4. At the end of the week, Jeffery calls `GET /challenges/weekly` and `GET /leaderboard/tags` to see what’s trending and how his challenge did.

---