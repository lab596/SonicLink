## Endpoint Timing

### Tags:


`/tags/leaderboard` Time: **0.513863** seconds

`/songs/love` Time: 0.008014 seconds

`/tags` Time: 0.008110 seconds

`/tags/upvote` Time: 0.038519 seconds

`/tags/users/3/tags` Time: 0.055154 seconds

`/tags/search?text=trade` Time: 0.211098 seconds

---
### Account:

`/account/new` Time: 0.240685 seconds

`/account/login` Time: 0.235448 seconds

---
### Challenges:

`/challenges/new` Time: 0.008019 seconds

`/challenges/5/submission` Time: 0.009187 seconds

`/challenges/weekly` Time: 0.119771 seconds

---

### Slowest Time:
 `/tags/leaderboard` Time: **0.513863** seconds

```bash
        Sort Key: (count(user_tag_upvotes.id)) DESC
        Sort Method: top-N heapsort  Memory: 26kB
        ->  GroupAggregate  (cost=137189.19..184603.71 rows=500000 width=55) (actual time=258.295..652.220 rows=432166 loops=1)
              Group Key: user_tags.id
              ->  Merge Join  (cost=137189.19..174604.20 rows=999901 width=51) (actual time=258.285..552.396 rows=1000002 loops=1)
                    Merge Cond: (user_tags.id = user_tag_upvotes.tag_id)
                    ->  Index Scan using user_tags_pkey on user_tags  (cost=0.42..18668.42 rows=500000 width=47) (actual time=0.019..37.935 rows=500001 loops=1)
                    ->  Materialize  (cost=137188.26..142187.77 rows=999901 width=8) (actual time=258.228..392.429 rows=1000002 loops=1)
                          ->  Sort  (cost=137188.26..139688.02 rows=999901 width=8) (actual time=258.225..330.964 rows=1000002 loops=1)
                                Sort Key: user_tag_upvotes.tag_id
                                Sort Method: external merge  Disk: 17704kB
                                ->  Seq Scan on user_tag_upvotes  (cost=0.00..23870.00 rows=999901 width=8) (actual time=0.017..127.266 rows=1000002 loops=1)
"                                      Filter: (""timestamp"" >= (now() - '7 days'::interval))"
Planning Time: 0.587 ms
JIT:
  Functions: 15
  Options: Inlining false, Optimization false, Expressions true, Deforming true
  Timing: Generation 0.248 ms (Deform 0.087 ms), Inlining 0.000 ms, Optimization 0.272 ms, Emission 6.423 ms, Total 6.944 ms
Execution Time: 722.266 ms
```
#### Analysis:

This means that the query had to run a full table scan over user_tag_upvotes and to speed up this query, we should index on tag_id and timestamp because we filter on by upvotes made in the last 7 days

---

### Create Index:
``` sql
CREATE INDEX idx_user_tag_upvotes_tagid_ts
ON user_tag_upvotes (tag_id, timestamp);
```

### After Index:
```bash
Limit  (cost=111559.41..111559.43 rows=10 width=55) (actual time=664.524..664.526 rows=10 loops=1)
  ->  Sort  (cost=111559.41..112809.41 rows=500000 width=55) (actual time=655.014..655.015 rows=10 loops=1)
        Sort Key: (count(user_tag_upvotes.id)) DESC
        Sort Method: top-N heapsort  Memory: 26kB
        ->  GroupAggregate  (cost=1.13..100754.59 rows=500000 width=55) (actual time=0.065..618.655 rows=432166 loops=1)
              Group Key: user_tags.id
              ->  Merge Join  (cost=1.13..90755.07 rows=999903 width=51) (actual time=0.049..506.664 rows=1000002 loops=1)
                    Merge Cond: (user_tag_upvotes.tag_id = user_tags.id)
                    ->  Index Scan using idx_user_tag_upvotes_tagid_ts on user_tag_upvotes  (cost=0.43..58339.30 rows=999903 width=8) (actual time=0.030..318.718 rows=1000002 loops=1)
"                          Index Cond: (""timestamp"" >= (now() - '7 days'::interval))"
                    ->  Index Scan using user_tags_pkey on user_tags  (cost=0.42..18668.42 rows=500000 width=47) (actual time=0.010..52.368 rows=500000 loops=1)
Planning Time: 0.555 ms
JIT:
  Functions: 14
  Options: Inlining false, Optimization false, Expressions true, Deforming true
  Timing: Generation 1.282 ms (Deform 0.620 ms), Inlining 0.000 ms, Optimization 0.396 ms, Emission 9.122 ms, Total 10.800 ms
Execution Time: 665.930 ms
```
#### Analysis:

The use of indexing reduced execution time. Before indexing, *722.266 ms*, and after indexing, *665.930 ms*. Thus this is what we expected by using indexing on user tag upvotes.
