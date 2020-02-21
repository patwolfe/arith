**Developing for JumboSmash**

*Running the server locally*

1. Make sure you're in the first `jumboSmash` directory (`arith/jumboSmash`)
2. Generate migrations: `python manage.py makemigrations [app name]` for each app (see app list below)
3. Run migrations: `python manage.py migrate`
4. Launch the server -- by default, it runs on localhost:8000: `python manage.py runserver`

*Running the server on the EC2 instance*
If you want to launch the server on AWS for testing, you should have a user on the ec2 instance and a key pair (if not, ping Caroline!). You should have the private key stored locally in a `.pem` file.  

SSH onto the server: `ssh -i [your private key].pem [your username]@jumbosmash-dev.us-east-1.elasticbeanstalk.com`
Once you are on the EC2 instance (you should see some funky ElasticBeanstalk ASCII art), cd to the shared `arith` directory (`../shared/arith` from your home directory) and follow the steps above to run the server. You may need to `pull` to ensure that the repo is up to date.


**Backend Architecture**

*Apps*
- Chat: contains match and messages functionality
- Swipe: interactions between users - skip or smash, block, report, retrieve users to swipe
- Auth
- User
- Admin

*API*
/chat
    /unmatch: mark this match as unmatched
    /send: post message
    /convo: retrieve all messages for this match
/swipe
    /smash: right swipe on a user
    /skip: left swipe on a user
    /get_next:  retrieve 10 users to swipe (not yet merged)
    /refresh: rebuild the deck for the current user so that they can see users they skipped previously (not yet merged)
    /block
    /top5
/auth
    /logout
/user
    /list: list all registered users
    /profile: retrieve profile for a given user
    /profile/edit: post profile changes
    /check: verify that a user (given email) exists in the database
