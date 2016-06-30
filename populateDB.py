#!/usr/bin/python

from werkzeug.security import generate_password_hash
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


def main():
    # Connect to the DB
    collection = MongoClient('52.23.231.5',27017)["restaurent"]["users"]

    # Ask for data to store
    user = "srini"
    password = "srini"
    role="manager"
    hotel="Barbeque Nation ( Indiranagar )"
    name="Srinivas Jayaram "
    email="srinii99@icloud.com"
    validity="01/12/2016"
    active="true"
    group=["Copper Chimney ( InOrbit Mall)", "Barbeque Nation ( Indiranagar )", "The Fisherman's wharf", "Little Italy", "Jalsa", "Hotel Empire", "Samarkand", "Coconut Groove", "Mast Kalandhar", "Koshy's"]

    pass_hash = generate_password_hash(password, method='pbkdf2:sha256')
    phone="+91-9912345612"
    # Insert the user in the DB
    try:
        collection.insert({"_id": user, "password": pass_hash,"role":role,"hotel":hotel,"name":name,"email":email,"validity":validity,"status":active,"group":group,'phone':phone})
        print "User created."
    except DuplicateKeyError:
        print "User already present in DB."


if __name__ == '__main__':
    main()
