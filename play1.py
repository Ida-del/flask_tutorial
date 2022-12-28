import json

user = json.loads('{"id": 1, "name": "John Doe", "email": ""}')

print(f'user name is {user["name"]}')
# print(f'user name is {user["name"]}')
# print(f'user name is {user["name"]}')
# print(f'user name is {user["name"]}')

def userinfo(u):
    id = u["id"]
    name = u["name"]
    return f'ID is {id} and name is {name}'

print(f'User Information: {userinfo(user)}')