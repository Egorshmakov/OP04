import re

my_str = "Hi my name is user1 and email address is user1@example.com and my friend's email is user2@gmail.com"
emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+[a-zA-Z0-9-.]+)", my_str)

for mail in emails:
    print(mail)
