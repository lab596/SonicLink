<h4> 12 user stories:</h4>

1. As a SonicLink user who uses music to express my identity, I want to be able to create `tags` to classify songs that I enjoy and share my thoughts with others. (write operation) <br/>

2. As a SonicLInk user who loves boosting others in the community, I want to be able to upvote tags I view if I enjoy what others have to say about a specific song. (write operation) <br/>

3. As a SoundLink user who enjoys tracking their influence and contributions, I want to be able to see the tags I created and how many likes they have received from others. (read operation) <br/>

4. As a SoundLink user who is always looking for new music vibes, I want to search for songs using specific tags so that I can find new music beyond traditional genres. (read operation) <br/>

5. As a SoundLink user who wants to meet like minded fans, I want to be recommended users (friends) that have had similar activity to me so that I can connect with people who have similar musical tastes. (read operation) <br/>

6. As a SoundLink user who enjoys understanding music through the lens of others, I want to see songs that other users have added to tags so that I can listen to music that others think matches the tag. (read operation) <br/>

7. As a SoundLink user who enjoys diving into the meaning of specific lyrics, I want to be able to write specific comments tagged to a specific timestamp on a song. (write operation) <br/>

8. As a SoundLink user who enjoys competing with friends, I want to be able to create a tag challenge that allows my community of friends to respond I create. (write operation) <br/>

9. As a SoundLinkuser who wants to participate in my friend's challenge, I want to be able to respond to my friend's challenge. (write operation) <br />

10. As a SoundLink user who values community input and creative competition, I want to be able to vote on responses to the challenge. (write operation) <br/>

11. As a SoundLink user who is interested in insights and outcomes of musical interactions, I want to be able to view the results of the challenge after it has been completed (read operation) <br />

12. As a SoundLink user who loves staying ahead of the music curve, I want to view songs sorted by most upvoted tags in the past week so I can stay on top of musical trends. (read operation)
    
13. As a SoundLink user who loves engaging with broader music trends, I want to see weekly challenges created by the community so I can participate in broader activity. (read operation)


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
  - A message will be shown with the error explaining to please choose a timestamp that matches the lyrics as well as select a moment within the song's duration. 

A searched song is not present in our Dataset.
  - A message will be shown saying we couldn't find that song, suggest search tips (ie. please check the title and spelling). 

A user tries to enter a challenge submission after the window closes.
  - A message will be shown with that explains the challenge window has closed and show when the window closed. 

A user tries to view their leaderboard without adding any tags.
  - A message will be shown saying they haven't tagged any songs, so there are no tags to display in the leaderboard.

A user tries to follow another user, but the action fails (network error or user deletion).
  - A message will be  shown asking the user to try again later or specifics about the users deletion

A user attempts to upvote their own tag.
  - A message will be shown explaining that upvoting one's own tag is not allowed to keep rankings fair

A user tries to view user's tags that has been deleted or suspended.
  - A "User's Tags Not Found because user doesn't exist" message will be shown and make suggestions for other users to follow

A user tries to access the leaderboard that has no tags on it.
  - A message will be shown stating: "Leaderboard doesn't currently have any tags." and will suggest the user to be the first to make a leaderboard worthy tag.
