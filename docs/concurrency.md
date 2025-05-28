# Concurrency in SonicLink

## 1. **Lost Update**

### Scenario

Two users try to upvote the same tag at the same time. Both read the current upvote count, increment it, and write back the result. Without concurrency control, one update is lost.

### Sequence Diagram

```
User A                Database                User B
  |                       |                     |
  |---Read upvotes------->|                     |
  |<--upvotes=5-----------|                     |
  |                                             |
  |                       |<---Read upvotes-----|
  |                       |---upvotes=5-------> |
  |                                             |
  |---upvotes=6---------->|                     |
  |                       |                     |
  |                       |<--upvotes=6-------- |
  |                       |                     |
  |                       |---upvotes=6-------->|
  |                       |                     |
```
**Result:** Both users see 5, both write 6. One increment is lost.

### Solution

- Use `SERIALIZABLE` isolation or optimistic locking (e.g., check the upvote count/version before updating).
- Use SQL: `UPDATE ... SET upvotes = upvotes + 1 WHERE ...` to ensure atomicity.

---

## 2. **Dirty Read** 

### Scenario

User A starts creating a challenge but hasn't committed yet. User B queries the weekly leaderboard and sees the uncommitted challenge. If User A rolls back, User B has seen data that never existed.

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

## 3. **Phantom Read**

### Scenario

User A queries all challenges for the leaderboard. User B creates a new challenge and commits. User A queries again in the same transaction and sees the new challenge.

### Sequence Diagram

```
User A                Database                User B
  |                        |                     |
  |---Begin Tx------------>|                     |
  |---Query challenges---> |                     |
  |<--[challenge 1,2]------|                     |
  |                        |---Begin Tx--------->|
  |                        |---Insert challenge->|
  |                        |---Commit----------->|
  |---Query challenges---> |                     |
  |<--[challenge 1,2,3]----|                     |
  |---Commit-------------> |                     |
```
**Result:** User A sees a "phantom" challenge appear during their transaction.

### Solution

- Use `REPEATABLE READ` or `SERIALIZABLE` isolation to prevent phantoms.
- For leaderboard queries, consider snapshot isolation or explicit locking if consistency is critical.

---

## Ensuring Isolation in SonicLink

- **Upvotes and similar counters:** Use atomic SQL updates or optimistic locking to prevent lost updates.
- **Challenge creation and leaderboard:** Use at least `READ COMMITTED` isolation to avoid dirty reads.
- **Leaderboard queries:** Use `REPEATABLE READ` or snapshot isolation if you need consistent results within a transaction.

