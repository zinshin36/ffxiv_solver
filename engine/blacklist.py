def is_blacklisted(item, blacklist):

    name = item["name"].lower()

    for bad in blacklist:

        if bad.lower() in name:
            return True

    return False
