# SonicLink API Specification

SonicLink is a backend API designed to enhance musical social interaction through tagging, challenges, and shared experiences.

## Base URL

`https://soniclink.com/v1/api`

---

## Endpoints 🎧

### 1. `POST /account/new`
**Create an account with SonicLink.**
**Request Body:**
```json
{
  "username": "myusername",
  "password": "mypassword"
}
```

**Responses:**
| Code | Description |
| --- | --- |
| 201 | Created |
| 422 | Validation Error |

#### Example Response:

```json
{
  "user_id": 123,
}
```

### 2. `GET /account/login`
**Login to an existing account to fetch the user id.**

**Request Body:**
```json
{
  "username": "myusername",
  "password": "mypassword"
}
```

**Responses:**
| Code | Description |
| --- | --- |
| 201 | Created |
| 4o1 | Unauthorized Error |
| 422 | Validation Error |

#### Example Response:

```json
{
  "user_id": 123,
}
```

## Tags

### 3. `POST /tags`
**Create a new tag for a song.**

**Request Body:**
```json
{
  "user_id": 123,
  "song_id": "spotify:track:xyz",
  "tag_text": "lowk a bop"
}
```
#### Example Response:

```json
{
  "tag_id": 123,
  "message": "Tag created successfully"
}
```
**Responses:**
| Code | Description |
| --- | --- |
| 201 | Created |
| 400 | Bad Request |
| 422 | Validation Error |

### 2. `POST /tags/upvote`
**Upvote an existing tag.**

**Request Body:**
```json
{
  "user_id": 123,
  "tag_id": 456,
}
```
#### Example Response:

```json
{
  "message": "Successfully upvoted!"
}
```


**Responses:**
| Code | Description |
| --- | --- |
| 202 | Accepted |
| 422 | Validation Error |

### 3. `GET /users/:user_id/tags`
**View all tags created by a user with total likes.**

**Responses:**
| Code | Description |
| --- | --- |
| 200 | Successful Response |     
| 404 | User not Found |

#### Example Response:

```json
[
  {
    "tag_text": "car bops",
    "song_id": "spotify:track:abc",
    "upvotes": 12
  },
  ...
]
```

### 4. `GET /tags/search?text={query_text}`
**Search for songs by tag text.**

* Note - will attempt to implement wildacards to enable searches of all tags

**Responses:**
| Code | Description |
| --- | --- |
| 200 | Successful Response |     

#### Example Response:

`/tags/search?text=sleepy`

```json
[
  {
    "song_id": "spotify:track:xyz",
    "title": "Twinkle Twinkle Little Star",
    "artist": "Jane Taylor",
    "tag": "sleepy time",
    "tag_id" : 123
  }
]
```
## Lyrical Moments

### 5. `POST /lyrical-moments`
**Add a lyrical moment to a song.**

**Request Body:**
```json
{
  "user_id": 321,
  "song_id": "spotify:track:xyz",
  "timestamp_seconds": 45,
  "lyric": "You only need the light when it's burning low",
  "moment_text": "hella deep bro"
}
```

**Responses:**
| Code | Description |
| --- | --- |
| 204 | Successful Response |
| 400 | Bad Request |
| 422 | Validation Error |

## Challenges

### 6. `POST /challenges`
**Create a new tag challenge.**

**Request Body:**
```json
{
  "user_id": 321,
  "title": "Best Summer Vibes",
  "description": "Tag songs that scream summer!"
}
```

**Responses:**
| Code | Description |
| --- | --- |
| 201 | Accepted |
| 422 | Validation Error |

#### Example Response:

```json
{
  "challenge_id": 123,
  "message": "Challenge created successfully"
}
```

### 7. `POST /challenges/:id/submission`
**Submit a tag to an existing challenge.**

**Request Body:**
```json
{
  "user_id": 123,
  "tag_text": "pool party anthem"
}
```

**Responses:**
| Code | Description |
| --- | --- |
| 204 | Successful Response |
| 404 | Challenge not Found |

### 8. `GET /challenges/weekly` (COMPLEX ENDPOINT)
**Get this week's public community challenges.**

**Responses:**
| Code | Description |
| --- | --- |
| 204 | Successful Response |
| 422 | Validation Error |

#### Example Response:

```json
[
  {
    "challenge_id": 666,
    "title": "Top Breakup Bangers",
    "created_by": "lovergone",
    "created_at": "2025-04-01"
  }
]
```

### 9. `GET /leaderboard/tags`
**Get top tags from the last week.**

**Responses:**
| Code | Description |
| --- | --- |
| 204 | Successful Response |
| 422 | Validation Error |

#### Example Response:

```json
[
  {
    "tag_text": "hype run",
    "upvotes": 123,
    "song_id": "spotify:track:def"
  }
  ...
]
```
### 10. `GET /recommended` (COMPLEX ENDPOINT)
**Get recommended users who have contributed to similar things as you.**

**Responses:**
| Code | Description |
| --- | --- |
| 204 | Successful Response |
| 404 | Not Found |

#### Example Response:

```json
[
  {
    "user_id": "123",
    "reccomened_users": {user_id,...,}
  }
  ...
]



