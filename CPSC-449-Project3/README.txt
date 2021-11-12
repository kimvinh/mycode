# Members: Vinh Tran (Email: kimvinh@csu.fullerton.edu)
	   Quang Nguyen (Email: quangdnguyen2211@csu.fullerton.edu)

# CPSC 449 - 02

# Professor: Kenytt Avery

# Project 2: Microservice Implementation and Load Balancing

----------------------------------------------------------------------------------------------------

### SUMMARY ###

- There are two main microservices built in this project, one for 'users' and one for 'timelines' to provide
the services to users. With the 'users' services, users can register, follow/ unfollow each other, post messages, and change their information (i.e., password, bio). With the 'timelines' services, they can show users' posts that they have made, all posts from all users that this user followed, and all posts from all users. There are some services that require users to log in before using. 

- For all new creations of a user or post, they will be stored in the database files. Each user created will have a username, a bio, an email address, and a password. Each post that a user creates will have the author's username, the text (content) of the post, and a timestamp.

- For production deployment, Gunicorn is used in this project as a WSGI server to run both microservices, and the program was designed to handle the running of multiple instances of the 'timeline' service by using HAProxy as an load balancer.

----------------------------------------------------------------------------------------------------

### MICROSERVICES - DETAILED DESCRIPTIONS ###

## 'Users' Microservices ##

1. @hug.get("/users/")

- This service will return all existing users from the database as a JSON format.

- To use the service in the browser, please type URL = "http://127.0.0.1/users/"

- To use the service through the terminal, please command: $ http 127.0.0.1/users/

2. @hug.get("/users/{username}")

- This service will retrieve the specific user based on 'username' as the endpoint. If found, the response status will be '200 OK' and return the specific user as a JSON format. Otherwise, the response status is '404 NOT FOUND'.

- To use the service in the browser, please type URL = "http://127.0.0.1/users/{username}"

- To use the service through the terminal, please command: $ http 127.0.0.1/users/{username}

3. @hug.get("/get-following/{username}")

- This service retrieves all users that a user follows based on 'username' as the endpoint from the databbase. Users will be returned as a JSON format.

- To use the service in the browser, please type URL = "http://127.0.0.1/get-following/{username}"

- To use the service through the terminal, please command: $ http 127.0.0.1/get-following/{username}

4. @hug.post("/create/", status=hug.falcon.HTTP_201)

- This service allows a user to create an account. A user's account will include a username, an email, a password, and a bio. If created successfully, the response status is '201 Created'. Otherwise, the response status is '409 Conflict' if a user tries to create an account that was already existed, and the error message will be returned.

- To use the service through the terminal, please use 'new_user.json' as an example.
In the terminal, please command: $ http --verbose POST 127.0.0.1/create/ @./share/new_user.json

5. @hug.put("/change-password/")

- This service allows an existing user to change their password. If changed successfully, the response status is ' 200 OK'. Otherwise, the response status is either '401 Unauthorized' or '404 Not Found' if inputs are incorrect.

- To use the service through the terminal, please use 'new_password.json' as an example.
In the terminal, please command: $ http --verbose PUT 127.0.0.1/change-password/ @./share/new_password.json

6. @hug.get("/login/")

- This service will verify the user's authentication by checking a user's username and password. If a user successfully logs in, they can access to some services that require the authentication. Otherwise, the response status is either '401 Unauthorized' or '404 Not Found' if inputs are incorrect, and the error message will be returned.

- To use the service in the browser, please type URL = "http://127.0.0.1/login?username={username}&password={password}"

- To use the service through the terminal, please command: http '127.0.0.1/login?username={username}&password={password}'

7. @hug.post("/follow/", status=hug.falcon.HTTP_201)

- This service allows an existing user to follow each other. If followed successfully, the response status is '201 Created'. Otherwise, the response status is '409 Conflict' if a user tries to follow another user that they already followed.

- To use the service through the terminal, please use 'new_follow.json' as an example.
In the terminal, please command: $ http --verbose POST 127.0.0.1/follow/ @./share/new_follow.json

8. @hug.post("/unfollow/")

- This service allows an existing user to unfollow each other. A user needs to provide their username and another user's username that they want to unfollow. If unfollowed successfully, the response status is '200 OK'. Otherwise, the response status is '409 Conflict' if a user tries to unfollow another user that they do not follow yet.

- To use the service through the terminal, please use 'new_follow.json' as an example.
In the terminal, please command: $ http --verbose POST 127.0.0.1/unfollow/ @./share/new_follow.json

9. @hug.put("/update-bio/")

- This service allows an existing user to update their bio. They need to provide their username and the text for their bio. If updated successfully, the response status is '200 OK'. Otherwise, the response status is '400 Bad Request' if inputs are incorrect or missing.

- To use the service through the terminal, please use 'new_bio.json' as an example.
In the terminal, please command: $ http --verbose PUT 127.0.0.1/update-bio/ @./share/new_bio.json

## 'Timelines' Microservices ##

1. @hug.get("/post/")

- This service will return all users' posts from the database as a JSON format.

To use the service in the browser, please type URL = "http://127.0.0.1/post/"

To use the service through the terminal, please command: $ http 127.0.0.1/post/

2. @hug.get("/userTimeline/{username}")

- This service will provide a user timeline by retrieving all posts that a user has made based on 'username' as the endpoint. If retrieved successfully, the response status is '200 OK', and all posts will be returned as a JSON format by the reverse chronological order. Otherwise, the response status is '404 Not Found' if the input is not correct, and the returned post is empty.

To use the service in the browser, please type URL = "http://127.0.0.1/userTimeline/{username}"

To use the service through the terminal, please command: $ http 127.0.0.1/userTimeline/{username}

3. @hug.get("/publicTimeline/")

- This service will retrieve all users' posts and return them in the reverse chronological order as a public timeline. If retrieved successfully, the response status is '200 OK', and all posts will be returned as a JSON format. Otherwise, the response status is '404 Not Found', and the returned post is empty.

To use the service in the browser, please type URL = "http://127.0.0.1/publicTimeline/"

To use the service through the terminal, please command: $ http 127.0.0.1/publicTimeline/

4. @hug.get("/homeTimeline/{username}", requires=authentication)

- This service allows an existing user to see all users' posts that they followed as a home timeline. However, they need to get the authorization to use the service by logging in. Also, they can only access their home timeline to themselves. If authenticated successfully, all users' posts that a user followed will be returned as a JSON format in the reverse chronological order. Otherwise, the response status is '404 Not Found' if an input is not correct, and the returned post is empty.

To use the service in the browser, please type URL = "http://127.0.0.1/homeTimeline/{username}"

To use the service through the terminal, please command: $ http --auth username:password 127.0.0.1/homeTimeline/{username}

5. @hug.post("/message/", requires=authentication)

- This service allows an existing user to post messages, but they need to get the authorization to do so by logging in and then input the text for the post. If authenticated successfully and inputted correctly, the response status is '201 Created', and the post will be returned as a JSON format. Otherwise, the response status is either '401 Unauthorized' due to the failure of login or '400 Bad Request' if the input is incorrect or missing.

To use the service through the terminal, please command: $ http --auth username:password POST 127.0.0.1/message/ text="{The text of the post}"

----------------------------------------------------------------------------------------------------

### REQUIREMENTS ###

- There are some tools and libraries needed to be installed before running the microservices:

   1. Hug
   2. sqlite-utils libraries
   3. HAProxy
   4. Gunicorn server

----------------------------------------------------------------------------------------------------

### "CPSC-449-Project2.tar.gz" Contents ###

1. README.txt				// This file

2. timelines_services.py		// Containing the source code that executes the 'timelines' services

3. user_services.py			// Containing the source code that executes the 'users' services

4. Profile				// Containing The WSGI-compatible server (Gunicorn) to run both microservices

5. .env					// Avoiding missing output from Foreman

6. "var" folder				// Containing the log and database files
   6.1. "log" folder			// Containing the log files of microservices
      6.1.1. user_services.log		// Containing records of activities within the 'users' microservice
      6.1.2. timelines_services.log	// Containing records of activities within the 'timelines' microservice
   6.2. posts.db			// The database file that stores all users' posts
   6.3. users.db			// The database file that stores all users' information and followings

7. "bin" folder				// Containing the shell files
   7.1. init.sh				// The shell script that initializes all database files
   7.2. posts.sh			// The shell script that run the specific command(s)

8. "etc" folder				// Containing the configuration files related to two microservices
   8.1. users_services.ini
   8.2. timelines_services.ini
   8.3. user_services_logging.ini
   8.4. timelines_services_logging.ini
   8.5. haproxy.cfg

9. "share" folder			// Containing the JSON and CSV files
   9.1. new_bio.json
   9.2. new_follow.json
   9.3. new_password.json
   9.4. new_user.json
   9.5. following.csv
   9.6. posts.csv
   9.7. users.csv

----------------------------------------------------------------------------------------------------

### HOW TO START THE SERVICES ###

# Note: The following steps will ask you to install some tools and libraries to meet the requirements
for running the project.

1. To install pip package installer and tools, command:

$ sudo apt update
$ sudo apt install --yes python3-pip ruby-foreman httpie sqlite3

2. To install Hug and sqlite-utils libraries, command:

$ python3 -m pip install hug sqlite-utils

3. To install the HAProxy and Gunicorn servers, command:

$ sudo apt install --yes haproxy gunicorn

4. To load the database for the services, command:

$ ./bin/init.sh

5. Please replace the content of 'haproxy.cfg' file in your system with the content of 'haproxy.cfg' in the "etc" folder.
   Then, to configure HAProxy to present as an HTTP load balancer, command:

$ sudo systemctl start haproxy

6. To start two microservices concurrently, command on another terminal:

$ foreman start --formation user_services=1,timelines_services=3
