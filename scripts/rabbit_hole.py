from bs4 import BeautifulSoup
import requests

key = 'cE4g5bWZtYCuovEgYSO1'
result = []

try:
    while True:
        session = requests.session()
        init = session.get(f'http://167.71.246.232:8080/rabbit_hole.php?page={key}')
        init_content = BeautifulSoup(init.content, 'html.parser')

        data = list(init_content.children)[0]
        code_string = data.split('\n ')[0]
        key = data.split('\n ')[1]

        code = code_string.strip('][').split(', ')
        print(f'appending {code}, generated with {key}')
        result.append(code)
except:
    print('parsing complete')

formatted_result = []
for i in result:
    temp = [int(i[0]), i[1].replace("'", '')]
    formatted_result.append(temp)

# Creating a list of None values
# e[0] is the location in memory, a value between 0 and 1582.
# The following places all values to their positions
flag = [None] * len(formatted_result)
for e in formatted_result:
    flag[e[0]] = int(e[1], 16)

f = open('flag.png', 'wb')
f.write(bytes(flag))
