import requests
from colorama import Fore, Back, Style

okb = Fore.BLUE
okg = Fore.GREEN
bright = Fore.WHITE
error = Fore.RED
endc = Fore.RESET


def import_keys():
    try:
        # Load own access token
        from keys import BASE_URL, APP_ACCESS_TOKEN
    except Exception:
        # If on remote use test access token
        print(Fore.RED + "Failed to fetch Access Token \nUsing test Account Token" + Fore.RESET)
        global APP_ACCESS_TOKEN, BASE_URL
        APP_ACCESS_TOKEN = "7036375990.cc65dcb.807e809e00f14248916c05c66db4d473"
        BASE_URL = 'https://api.instagram.com/v1/'
        print(okg + "test account loaded" + endc)


def info(name="self"):
    request_url = (BASE_URL + 'users/'+name+'/?access_token=%s') % APP_ACCESS_TOKEN
    # print('GET request url : %s' % (request_url))
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        print('Username: %s' % (user_info['data']['username']))
        print('No. of followers: %s' % (user_info['data']['counts']['followed_by']))
        print('No. of people you are following: %s' % (user_info['data']['counts']['follows']))
        print('No. of posts: %s' % (user_info['data']['counts']['media']))
    else:
        print(Fore.LIGHTRED_EX + 'Something went wrong' + Fore.RESET)


def get_user_id(insta_username):
    """
    Method to get User Id by providing instagram username
    """
    request_url = (BASE_URL + '/users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print('Requesting info for:' + request_url)
    search_results = requests.get(request_url).json()
    if search_results['meta']['code'] == 200:
        if len(search_results['data']):
            return search_results['data'][0]['id']
        else:
            print(error+'User does not exist!'+endc)
    else:
        print('Error Fetching username')
        return None


def search_user():
    info("user")


def view_post():
    pass


def make_comment():
    pass


def show_liked_posts():
    pass


def comment_on_post():
    pass


def delete_neg_comment():
    pass


def load_index():
    menu = "1.View your profile\n2.Search User by username\n3.Get your recent post\n4.Make comment on recent " \
           "post\n5.Get liked posts of user\n6.Comment " \
           "on post\n7.Delete negative comment\n8.Exit\n"
    ch = input(menu)

    options = {
        1: info,
        2: search_user,
        3: view_post,
        4: make_comment,
        5: show_liked_posts,
        6: comment_on_post,
        7: delete_neg_comment,
        8: exit
    }
    options[int(ch)]()


if __name__ == '__main__':
    print(okb + "Welcome to InstaBot" + endc)
    import_keys()
    load_index()
    # self_info()
