import re

string = "Это пример текста, в котором мы ищем слово Python"
result = re.findall(r'\w+$', string)
print(result)