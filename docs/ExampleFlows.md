# SonicLink Example Flows

---

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

## Flow 2: Community Challenge Participation 🎯

Jeffery Bezos wants to kick off a friendly tagging contest around sad songs that feel empowering.

1. Leo calls `POST /challenges` with:
   - title: "Sad but Strong"
   - song_id: "spotify:track:def789"

2. His friend Elon participates by calling `POST /challenges/789/submissions` with:
   - tag_text: "cry then conquer"

3. Other users vote on Elon's tag via `POST /tags/upvote`.

4. At the end of the week, Jeffery calls `GET /challenges/weekly` and `GET /leaderboard/tags` to see what’s trending and how his challenge did.

---
## Flow 3: Linking with Other Users 👯

Tony Stark has been listening to a lot of music, but he's feeling a little lonely with all of the Avengers mad at him. He wants to be recommeneded other Sonic Link users who enjoy similar music.

1. Tony calls `POST /tags` with:
   - user_id: 4
   - song_id: "spotify:track:abc123"
   - tag_text: "Genius, Billionaire, Playboy, Philanthropist"

2. His friend Pepper Potts calls `POST /tags` with:
   - user_id: 5
   - song_id: "spotify:track:abc456"
   - tag_text: "Smart, Rich, Playa, Humanitarian"

3. Pepper Potts also calls `POST /tags/upvote` on the tag that Tony made because she enjoys the song.

4. Tony then calls `GET /recommended` and is returned Pepper Potts' user_id, because she upvoted his tag and made her own tag with similar wording.

5. Tony can now call  `GET /users/:user_id/tags` with Pepper's user_id and see the music she's been enjoying and hopefully find new music.

---
