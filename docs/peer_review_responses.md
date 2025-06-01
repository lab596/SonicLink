# Code Review Comments:


### Lucas Pierce:
- It is quite hard to use the API with no way to search songs. I was able to make it work by going into your manual test example to find song ids, but this threw off your other testers.
  - Already addressed
  
- Recommendations doesn’t seem to do anything. Even when I add songs to tag, it still just gives me nothing.
  - ### needs to be addressed
  
- The rest of the endpoints worked for me, but the other testers got 500 errors that you should resolve if you haven’t already.
  - Already addressed
  
- Don’t store passwords in plaintext. I prefer you have no passwords at all rather than have poor password handling.
  - Already addressed

---
### Adam Kong:
- In User it’s possible to have a duplicate account with the same information with different id’s. Possibly look into creating only unique usernames so they don’t conflict
  - Already addressed


- In the with block for creating user id’s, even checking the database system and where using .fetchone(), look into using .scalar_one() and .scalar_one_or_none() instead of using .one() to grab the single id since it’s already returning an id.
  - Already addressed
 
    
- Update so the potionshop details are removed in server.py
  - Already addressed
 
    
- Confused on how lyrical moments are used for recommending songs, add more clarification to the use.
  - ### Need to be addressed

---
### Mehek Bhargava:
- There is no enforcement of unique usernames in the account_users table. Updating the schema to sa.Column("username", sa.String, unique=True, nullable=False) would prevent duplicates.
  - Already addressed
 
    
- If you add a unique constraint on usernames, creating a user with a duplicate username will cause an error. Adding a try/except block in create_new to catch this and return an error message like “Username already taken” would fix this.
  - Already addressed
    
- The ChallengeResponse model is defined but not used anywhere in challenges.py. Consider removing it if it’s not needed.
  - Already addressed
    
- In lyricalmoments.py, the create_moment function prints song_duration[0] before checking if song_duration or song_duration[0] exists. If this was used for debugging, consider removing it to avoid errors.
  - Already addressed
    
- The song_timestamp column of the lyrical_moments table is created to store a string in the schema, but your code uses an integer for seconds in the MomentCreateRequest model. Consider using the same type in both places (integer is probably better).
  - ### Need to be addressed
    
- You select track_id from the user_tags table in the recommend function but don’t use it later. Consider removing it if it’s unnecessary.
  - Already addressed
    
- In the recommend function, you don’t check if the user exists. Since you do this in other files, I would recommend adding the same check here.
  - Already addressed
    
- In recommended, if a user has no tags, the function returns an empty list. However, returning an empty list could also mean that no recommendations met the similarity threshold. Consider returning a message to clarify which scenario applies.
  - Already addressed

---
### Kenton Rhoden:
- Try to keep the naming conventions consistent with endpoints for readability. to create a new account it's /account/new but to create a new challenge or tag it's /challenges and /tags. I personally like having the /new included, but either way, the naming should be consistent
  - Already addressed
 
- description comment of create_moment function for the endpoint /lyrical-moments says its creating a new tag for a song instead of saying that it creates a new moment
  - Already addressed

---
### Vic Gregory:
- recommended: I don’t know how long it takes for the Levenshtein function to calculate the similarity, but if it takes a significant amount of time it might be helpful to write a simpler function (bare bones, like sharing more than two or three characters) and use levenshtein for the ones that are more similar. If there are many tags per user and there are many users, it may take a while for all of these to generate.
  - Already addressed
    
- server: The description still refers to the potion shop.
  - Already addressed
    
- tags: Same request here from above with TagCreateRequest and UpvoteRequest.
  - Already addressed
    
- tables: It seems like the usernames are able to be duplicated. Setting these as a unique constraint would remove this (and would allow for user search without the ID, helpful for user functions versus search functions).
  - Already addressed
    
- tables: There’s a mismatch between the type of song_timestamp and the type that is passed to it (string vs integer).
  - ### Need to be addressed

---
## Not going to address:
- Create_upvote appears to creates an error if either tag id or user id doesn’t exist.
- In the submit_challenge function, it returns nothing
- No checking if there can be multiple upvotes for the same tag? This could be an oversight if the number of upvotes affect the recommended score.
- Format is inconsistent across all source files. Consistent formatting would help readability, get_leaderboard in tags.py is formatted improperly,
- Checking for username or password in the login should differentiate if password or username doesn't exists rather than saying not finding both.
- Code is not documented, although functions have a clear use
- Questioned the purpose of the login function, login returns only id? Can there be another purpose?
- Add proper test files for API. Currently all potionshop test like barrels and bottlers test
  - Out of scope
- In account.py, the response model Creationresponse is used for both create_new and login_user, but its name implies it’s only for creation. Renaming it to something more general like UserIdResponse would make it clearer.
  - No lb
- In challenges.py, the create_challenge docstring says “Recommends users that have made a tag with the same song or same tag title,” which doesn’t match the endpoint’s purpose of creating a new challenge.
  - Not worth time
- In lyricalmoments.py, the create_challenge docstring says “Create a new tag for a song,” but the endpoint actually creates a new lyrical moment.
- No check exists that prevents a user from making the same lyrical moment for the same song multiple times. Adding a check for existing rows with the same user_id, track_id, and song_timestamp would fix this.
- the class User should have a more descriptive name and potentially be separated into 2 classes. You will probably have to store more information in the account_users table than just the username and password, but you use that same class for logging in. I suggest having separate classes for account creation and logging in
  - Out of scope
- Creationresponse may need to be separated too. Look into having different classes for the responses to creating an account and logging in to an account. Also, you may want to consistently use some casing convention that distinguishes between words for readability (like camel case)
  - Out of scope
- description comment of create_challenge function for the endpoint /challenges does not match the actual purpose of that endpoint
- you could use "SELECT EXISTS (*subquery*)" for your /challenges endpoint query (and any other endpoint that checks existence), which will return a boolean telling you whether your subquery has at least one result. This is more efficient than returning the entire row
- The function submit_challenge for endpoint /challenges/{challenge_id}/submission does not return anything. You should put some sort of return. Also, you may want to try adding function return type annotation, which just specifies what the return type of a function should be.
  - Not supposed to return anything
- you could do a try/except statement instead of doing a query every time you want to check if an id exists before linking it to a foreign key. You would just need to catch the errors where there is a foreign key violation, and that would serve as your existence check.
  - Could lead to wrong error messages
- the class MomentCreateRequest has an attribute song_id which is supposed to represent the track_id in your database. For readability, it might be helpful to make their variable names the same, unless you have some reason not to. This same thing shows up in tags.py too
- Consider adding tests for your code. Currently you have the stuff from the potion shop still
  - Out of scope
- account: If any changes could be made, it would be to force the user to log in before they get their ID for extra security and to make sure their password is correct.
- challenge: This looks fine, error handling looks comprehensive. I do think that the endpoints could have separate fields for the SubmissionRequest and ChallengeRequest classes, so it’s easier to see which fields you need to fill out.
- lyricalmoments: Same request here from above with MomentCreateRequest.
- lyricalmoments: It appears the table for the lyrical moments doesn’t enforce uniqueness for the song_id and song_timestamp for a user, so there can be multiple lyrical moments at the same place. This might be intentional though.
  - Intentional
- general: Some of the functions don’t have full error handling (ex: lyricalmoment, recommend, tags).
- general: It would help to have more comments in the functions for better readability.
- general: No unit tests for the basic / no SQL functions. It might also help to separate the SQL portions from the non SQL portions for ease of testing (similar to create_potion_plan and get_potion_plan).
- Are there ways to update new songs in the database? Considering the kaggle the dataset is from was last updated 3 years ago, current popular songs since 2022 have not been included.
  - Out of scope


