<h4> 12 user stories:</h4>

* As a user, I want to be able to create `tags` to classify songs that I enjoy and share my thoughts with others. (write operation) <br/>
* As a user, I want to be able to upvote tags I view if I enjoy what others have to say about a specific song. (write operation) <br/>
* As a user, I want to be able to see the tags I created and how many likes they have received from others. (get operation) <br/>
* As a user, I want to search for songs using specific tags so that I can find new music beyond traditional genres. (get operation) <br/>
* As a user, I want to be recommended users (friends) that have had similar activity to me so that I can connect with people who have similar musical tastes. (get operation) <br/>
* As a user, I want to see songs that other users have added to tags so that I can listen to music that others think matches the tag. (get operation) <br/>
* As a user who enjoys specific lyrics, I want to be able to write specific comments tagged to a specific timestamp on a song. (write operation) <br/>
* As a user who enjoys competing with friend, I want to be able to create a tag challenge that allows my community of friends to respond I create. (write operation) <br/>
* As a user who wants to participate in my friend's challenge, I want to be able to respond to my friend's challenge. (write operation) <br />
* As a user who created the challenge or participated in a challenge, I want to be able to vote on responses to the challenge. (write operation) <br/>
* As a user who created the challenge or participated in a challenge, I want to be able to view the results of the challenge after it has been completed (get operation) <br />
* As a user, I want to view songs sorted by most upvoted tags in the past week so I can stay on top of musical trends. (get operation) 
* As a user, I want to see weekly challenges created by the community so I can participate in broader activity. (get operation)


<h4> 12 exceptions: </h4>
  
A search for song by tag returns nothing.
  - There will be a clear message that explains that the tag has no songs yet added to it and recommends that the user add a song
  
A user's tag creation fails.
  - There will be a clear message with the error (ie. Your tag exceeds the character limit. Please stay within 50 characters)

No user recommendations have been made.
  - A message will be shown stating that to get recommendations, the user needs to interact more by adding more songs to tags, creating tags, or just searching for music.

Recommendations don't seem like the users have similar tastes.
  - The data that was used to make that recommendation will be stated (ie. You were recommended this user because of your interest in the #Summer2025 tag)

A lyrical moment is submitted with an invalid timestamp.
  - A message will be shown with the error explaining to please choose a timestamp that matches the lyrics as well as select a moment within the songs duration. 

A searched song is not present in our Dataset.
  - A message will be shown saying we couldnt find that song, suggest search tips (ie. please check the tittle and spelling). 

A user tries to enter a challenge submission after window closes.
  - A message will be shown with that explains the challenge window has closed and show when the window closed. 

A user tries to view their leaderboard without adding any tags.
  - A message will be shown saying they havent tagged any songs so there are no tags to display in the leaderboard.  

