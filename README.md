# SonicLink

Welcome to SonicLink! A backend API built for the purpose of musical social interaction.

---

## 📌 Overview

The goal of SonicLink is to use existing music based datasets such as [Spotify Music Dataset](https://www.kaggle.com/datasets/solomonameh/spotify-music-dataset) to create meaningful connections based on interactions with songs. By making unique `tags` and  `likes`, users can be matched to others by the songs they enjoy. Building a whole new level of musical interaction!

### 🏷️ What are tags?
 Tags are meant to be community generated quips that users can attach to a specific song. They are meant to classify songs in a fun a playful manner to express interest or connections. 

 Tags enable interaction by allowing others who agree with a specific tag on a song to upvote the tag.

 ### 🎵 Wait what about lyric moments?
 Users can also express themselves through lyrical moments which are quips associated to specific lyrics in a song - allowing for more modular expression.


### 👥Social Interaction
Now that users can add tags and likes to a song how can they interact with others? 

Tag Leaderboards enable users to view their top upvoted tags as well as tags that others placed that are big hits!

Users can follow other users getting a constant feed of `tags` from their friends. Users can also participate in challenges made by friends to farm aura among friends.

# Schema

## Tables

### External Database

Imported Spotify dataset (read-only). Not maintained by our system. Used for reference.

    spotify_songs

### Users

Holds the registered users of SonicLink

Fields:

    id : Primary Key
    username : String
    email : String
    timestamp : Time

### Tags
User-generated tags attached to songs.

    id : Primary Key
    song_id : Foreign Key
    user_id : Foreign Key
    tag_text : String
    timestamp : Time

### Upvotes
Users can upvote tags they like. We are putting this in a join table to prevent a user from multiple upvotes on a tag.

    id : Primary Key
    tag_id : Foreign Key
    user_id : Foreign Key

### Lyrical Moments
Highlights of lyrics/moments users associate with songs.

    id : Primary Key
    song_id : Foreign Key
    user_id : Foreign Key
    timestamp_seconds : Integer
    lyric : String
    tag : String
    timestamp : Time

### Challenges
Curated tagging challenges for community participation.

    id : Primary Key
    title : String
    description : String
    song_id : Foreign Key
    user_id : Foreign Key
    timestamp : Time

### Challenge Submissions
Tags submitted in response to a challenge.

    id : Primary Key
    challenge_id : Foreign Key
    user_id : Foreign Key
    tag_text : String
    timestamp : time


---

# Contributers

Rohan Udupa : rudupa@calpoly.edu </br>
Anna Grillo : argrillo@calpoly.edu </br>
Kip Stackle : kstackle@calpoly.edu </br>
Felipe Rotelli: frotelli@calpoly.edu



