import configparser
import logging.config

import hug
import sqlite_utils

import requests

# Load configuration
#
config = configparser.ConfigParser()
config.read("./etc/api.ini")
logging.config.fileConfig(config["logging"]["config"], disable_existing_loggers=False)


# Arguments to inject into route functions
#
@hug.directive()
def sqlite(section="sqlite", key="dbfile", **kwargs):
    dbfile = config[section][key]
    return sqlite_utils.Database(dbfile)

@hug.directive()
def log(name=__name__, **kwargs):
    return logging.getLogger(name)

# Routes
#
@hug.get("/users/")
def users(db: sqlite):
    return {"users": db["users"].rows}

@hug.get("/users/{username}")
def retrieve_users(response, username: hug.types.text, db: sqlite):
    users = []
    try:
        user = db["users"].get(username)
        users.append(user)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"users": user}

# Create new user
@hug.post("/create/", status=hug.falcon.HTTP_201)
def create_user(
    response,
    username: hug.types.text,
    email_address: hug.types.text,
    password: hug.types.text,
    bio: hug.types.text,
    db: sqlite):

    users_db = db["users"]
    user = {
        "username": username,
        "email_address": email_address,
        "password": password,
        "bio": bio
    }

    try:
        users_db.insert(user)
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}

    # response.set_header("Location", f"/users/{user['id']}")
    return user

#Change Password
@hug.post("/change_password/", status=hug.falcon.HTTP_200)
def change_password(
    response,
    username: hug.types.text,
    old_password: hug.types.text,
    new_password: hug.types.text,
    db: sqlite):

    users_db = db["users"]
    try:
        user = users_db.get(username)
        if old_password == user["password"]:
            users_db.update(username, {"password": new_password})
        else:
            response.status = hug.falcon.HTTP_401
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404

#Check password
@hug.get("/login/")
def login(request, response, db: sqlite):
    users_db = db["users"]
    try:
        user = users_db.get(request.params["username"])
        if request.params["password"] != user["password"]:
            response.status = hug.falcon.HTTP_401
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_401
        return {'Authentication': response.status}
    return user

# Follow new user
@hug.post("/follow/", status=hug.falcon.HTTP_201)
def add_follow(
    response,
    username: hug.types.text,
    following: hug.types.text,
    db: sqlite):

    try:
        db["follows"].insert({"username": username,"following": following})
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
        return {"error": str(e)}

    return {"username": username,"following": following}

# Unfollow user
@hug.post("/unfollow/", status=hug.falcon.HTTP_200)
def unfollow(
    response,
    username: hug.types.text,
    following: hug.types.text,
    db: sqlite):

    try:
        db["follows"].delete((username, following))
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
        return {"error": str(e)}

# Change bio
@hug.post("/change_bio/", status=hug.falcon.HTTP_200)
def change_bio(
    response,
    username: hug.types.text,
    bio: hug.types.text,
    db: sqlite):

    try:
        db["users"].update(username, {"bio": bio})
    except Exception as e:
        response.status = hug.falcon.HTTP_404
        return {"error": str(e)}
