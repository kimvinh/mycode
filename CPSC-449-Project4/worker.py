# Members: Quang Nguyen, Vinh Tran
# CPSC 449
# Project 4: Asynchronous Processing


import hug
import sqlite_utils
import configparser
import logging.config
import requests
import os
import socket
import greenstalk
import json
import time
import re

# Load configuration
#
config = configparser.ConfigParser()
config.read("./etc/timelines_services.ini")
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

db = sqlite()
posts = db["post"]

pattern = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"

with greenstalk.Client(('127.0.0.1', 11300)) as client:
    while 1:
        job = client.reserve()
        post = json.loads(job.body)

        validation = re.findall(pattern, post["text"])
        if len(validation) > 0:
            r = requests.get(f'{validation[0]}')
            if r.json() == {}:
                client.delete(job)
                continue;

        try:
            posts.insert(post)
            post["id"] = posts.last_pk
        except Exception as e:
            print("error:", str(e))

        client.delete(job)
