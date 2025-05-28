# Concurrency in SonicLink

## 1. **Phantom Read On Upvote** 

### Scenario

One user is attempting to retieve their tags and its number of upvotes while another user is attempting to upvote said tag. If user one reads the number of rows from the `user_tags_upvotes` table, but then process T1 gets switched to user two who upvotes that tag. Rerunning the read of `user_tags_upvotes` in T1 will be a different reseult. Without concurrency control, the tag upvotes are inconsistent.

### Sequence Diagram

```
User A                Database                User B
  |                       |                     |
  |---Read upvotes------->|                     |
  |<--upvotes=5-----------|                     |
  |                       |                     |
  |                       |<--upvotes=6---------|
  |                       |                     |
  |---Read upvotes------->|                     |
  |<--upvotes=6-----------|                     |
  |                       |                     |
  |                       |                     |
```
**Result:** When user one does the exact same read call it returns a different value.

### Solution

- Use `REPEATABLE READ` or `SERIALIZABLE` isolation to prevent phantoms.

---

## 2. **Dirty Read On Challenge Creation** 

### Scenario

User A starts creating a challenge adn it is inserted into the challenge table but hasn't committed yet. User B queries the weekly leaderboard and sees the uncommitted challenge. If User A rolls back, User B has seen data that never existed.

### Sequence Diagram

```
User A                Database                User B
  |                       |                     |
  |---Begin Tx----------->|                     |
  |---Insert challenge--> |                     |
  |                       |<---Query leaderboard|
  |                       |---Return challenge->|
  |---Rollback----------->|                     |
```
**Result:** User B sees a challenge that is rolled back.

### Solution

- Use `READ COMMITTED` or higher isolation so queries only see committed data.

---

## 3. **Phantom Read In Tag Leaderboards**

### Scenario

User one queries the top tags using the leaderboard endpoint. User two upvotes a new tag that causes a shift in the leaderboard. User one queries leaderboard endpoint again in the same tranasaction and the result is not the same.

### Sequence Diagram

```
User A                Database                User B
  |                        |                     |
  |---Begin Tx------------>|                     |
  |---Query leaderboard--->|                     |
  |<--[tag 1,2]------------|                     |
  |                        |---Begin Tx--------->|
  |                        |---Upvote Tag------->|
  |                        |---Commit----------->|
  |---Query challenges---> |                     |
  |<--[tag 1,2,3]----------|                     |
  |---Commit-------------> |                     |
```
**Result:** User one sees a "phantom" tag appear during their transaction.

### Solution

- Use `REPEATABLE READ` or `SERIALIZABLE` isolation to prevent phantoms.
- For leaderboard queries, consider snapshot isolation or explicit locking if consistency is critical.

---

## Ensuring Isolation

- **Upvotes and similar counters:** Use atomic SQL updates or optimistic locking to prevent lost updates.
- **Challenge creation and leaderboard:** Use at least `READ COMMITTED` isolation to avoid dirty reads.
- **Tag Leaderboard queries:** Use `REPEATABLE READ` or snapshot isolation if you need consistent results within a transaction.

