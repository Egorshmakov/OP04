import re


def change_date_format(dt):
        return re.sub(r'(\d{1,2}).(\d{1,2}).(\d{4})', '\\3-\\2-\\1', dt)


dt1 = "25.12.2022"
print("Original date in dd.mm.yyyy Format: ", dt1)
print("New date in yyyy-mm-dd Format: ", change_date_format(dt1))