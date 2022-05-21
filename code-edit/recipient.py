import requests
from bs4 import BeautifulSoup

def check_license():
    ##
    try:
        url = 'https://akylinandrej.wixsite.com/colden-i/key-passwd'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('div',id="comp-kzgj4ji2")
        ##
        line_1=str(quotes)
        line_1=line_1.split("\\")[1]
        len_O = len(line_1)
        cod=""
        inn=0
        for i in line_1:
            inn+=1
            cod += str(ord(i))
            if inn < len_O: cod+="@"
        cod+="*"+cod
        return str(cod)
    except ConnectionError:
        return "error"



def check_update():
    url = 'https://akylinandrej.wixsite.com/colden-i/key-passwd'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('div', id="comp-kzgj5gmp")
    ##
    line_1 = str(quotes)
    line_1 = line_1.split("\\")[1]


    return str(line_1)
