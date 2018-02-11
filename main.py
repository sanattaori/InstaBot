import requests
from colorama import Fore, Back, Style

try:
    from keys import BASE_URL, APP_ACCESS_TOKEN
except Exception:
    print(Fore.RED+"Failed to fetch Access Token \nUsing test Account Token"+Fore.RESET)
    print("Loading test account")
    APP_ACCESS_TOKEN = "7036375990.cc65dcb.807e809e00f14248916c05c66db4d473"
    BASE_URL = 'https://api.instagram.com/v1/'


def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % APP_ACCESS_TOKEN
    # print('GET request url : %s' % (request_url))
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        print('Username: %s' % (user_info['data']['username']))
        print('No. of followers: %s' % (user_info['data']['counts']['followed_by']))
        print('No. of people you are following: %s' % (user_info['data']['counts']['follows']))
        print('No. of posts: %s' % (user_info['data']['counts']['media']))
    else:
        print('Error invalid token')


self_info()