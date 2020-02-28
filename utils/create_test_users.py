import json

names_file = open("../parsed_class_of_2020.csv", "r")
dummy_users = []
names_file.readline()
count = 0
for line in names_file:
    count += 1
    info = line.split(",")
    fields = {
        "password": "555666",
        "last_login": None,
        "is_superuser": True,
        "first_name": info[2],
        "last_name": info[3],
        "is_staff": False,
        "is_active": False,
        "date_joined": "2011-07-14T19:43:37+0100",
        "email": info[0].lower(),
        "groups": [],
        "user_permissions": [],
        "status": "User.ACTIVE",
    }
    user = {"model": "users.user", "pk": count, "fields": fields}
    dummy_users.append(user)

outfile = open("../jumboSmash/tests/large_test_users.json", "w+")
json.dump(dummy_users, outfile)
