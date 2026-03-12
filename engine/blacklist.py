def is_blacklisted(item, blacklist):

    name = item["name"].lower()

    for b in blacklist:

        if b.lower() in name:
            return True

    return False
