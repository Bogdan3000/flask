import subprocess
try:
    import flask
except ImportError:
    subprocess.check_call(['pip', 'install', 'flask'])
    import flask
try:
    import requests
except ImportError:
    subprocess.check_call(['pip', 'install', 'requests'])
    import requests
try:
    import json
except ImportError:
    subprocess.check_call(['pip', 'install', 'json'])
    import json
try:
    import functools
except ImportError:
    subprocess.check_call(['pip', 'install', 'functools'])
    import functools
import json
from flask import Flask, render_template, request
import requests
from functools import lru_cache


app = Flask(__name__)

def get_vk_user_info(vk_id):
    access_token = 'vk1.a.bKCxYX48OTt3T2Cw5xxLKdLmHAA5b9M2OYjR9AwptUwvkf8bQwYOZVyLKEYY7gKSz1JeLpP8dZcpzF1lBWfECzJYlKiAJSh9eSm7Yxfuu_fddXUEQm5kjezK1bydTeIb_dW3W9t0_t8C62UvWYMxDK6L0oo5l68gZ1VenssBzGAz9br-OLJQBRA-Ya_ok2p-VTWzKe_fohu4CYA8SmWVmA'
    api_version = '5.199'

    response = requests.get(
        f'https://api.vk.com/method/users.get?user_ids={vk_id}&fields=photo_100,screen_name&access_token={access_token}&v={api_version}')
    data = response.json()

    if 'response' in data:
        user_info = data['response'][0]
        return {
            'photo': user_info.get('photo_100'),
            'name': user_info.get('first_name'),
            'surname': user_info.get('last_name'),
            'vk_link': f'https://vk.com/{user_info.get("screen_name")}'
        }
    return None
def search_user_list(user_list, search_term):
    return [user for user in user_list if
            search_term.lower() in user['vk'].lower()
            or search_term.lower() in user['discord'].lower()
            or search_term.lower() in user['minecraft'].lower()
            or search_term.lower() in cached_get_vk_user_info(user['vk'])['name'].lower()
            or search_term.lower() in cached_get_vk_user_info(user['vk'])['surname'].lower()
            or search_term.lower() in cached_get_vk_user_info(user['vk'])['vk_link']]

# Декоратор lru_cache кэширует результаты вызовов функции в памяти
@lru_cache(maxsize=128)
def cached_get_vk_user_info(vk_id):
    return get_vk_user_info(vk_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    if request.method == 'POST':
        menu_option = request.form['menu_option']

        if menu_option == 'list':
            with open('data.json', 'r') as json_file:
                user_list = json.load(json_file)

            search_term = request.form.get('search', '')
            if search_term:
                user_list = search_user_list(user_list, search_term)

            for user in user_list:
                user_info = cached_get_vk_user_info(user['vk'])
                if user_info:
                    user.update(user_info)

            return render_template('result.html', user_list=user_list)

@app.route('/process_form_2', methods=['POST'])
def process_form_2():
    if request.method == 'POST':
        menu_option = request.form['menu_option']

        if menu_option == 'list':
            with open('data.json', 'r') as json_file:
                user_list = json.load(json_file)

            search_term = request.form.get('search', '')
            if search_term:
                user_list = search_user_list(user_list, search_term)

            for user in user_list:
                user_info = cached_get_vk_user_info(user['vk'])
                if user_info:
                    user.update(user_info)

            return render_template('table.html', user_list=user_list)

if __name__ == '__main__':
    app.run(debug=True)
