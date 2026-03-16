import csv
import json
from faker import Faker

fake = Faker()

def make_users(n=10):
   users= []
   for _ in range(n):
        users.append({"first name": fake.first_name(),
                   "last name": fake.last_name(),
                   "email": fake.email()
                })
        return users
if __name__ == "__main__":
    users = make_users(20)

    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

    with open("users.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=users[0].keys())
        w.writeheader()
        w.writerows(users)

    print("Created users.json and users.csv")

