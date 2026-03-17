import os

def load_blacklist():

    if not os.path.exists("blacklist.txt"):
        return []

    with open("blacklist.txt","r",encoding="utf8") as f:
        return [x.strip().lower() for x in f.readlines() if x.strip()]


def is_blacklisted(name, blacklist):

    name = name.lower()

    for word in blacklist:
        if word in name:
            return True

    return False
