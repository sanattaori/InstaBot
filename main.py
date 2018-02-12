import requests
from urllib.request import urlretrieve
from colorama import Fore

from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

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
        choice = input("Do you want to continue with test account (y/n)")
        if choice == "y" or choice == "Y":
            APP_ACCESS_TOKEN = "7036375990.cc65dcb.807e809e00f14248916c05c66db4d473"
            BASE_URL = 'https://api.instagram.com/v1/'
            print(okg + "test account loaded" + endc)
        else:
            APP_ACCESS_TOKEN = input("Enter Your API access token")
            BASE_URL = 'https://api.instagram.com/v1/'
            info()


def info(name="self", uid=''):
    if uid is None:
        exit()
    elif name == "self":
        request_url = (BASE_URL + 'users/' + name + '/?access_token=%s') % APP_ACCESS_TOKEN
    else:
        request_url = (BASE_URL + 'users/%s?access_token=%s') % (uid, APP_ACCESS_TOKEN)

    print('GET request url : %s' % request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        print('Username: %s' % (user_info['data']['username']))
        print('No. of followers: %s' % (user_info['data']['counts']['followed_by']))
        print('No. of people you are following: %s' % (user_info['data']['counts']['follows']))
        print('No. of posts: %s' % (user_info['data']['counts']['media']))
    else:
        print(Fore.LIGHTRED_EX + 'Something went wrong' + Fore.RESET)
        print(Fore.LIGHTYELLOW_EX + 'Invalid api key entered' + Fore.RESET, end=error + "\nExiting" + error)
        exit()


def get_user_id(insta_username):
    """
    Method to get User Id by providing instagram username
    """
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print('Requesting info for:' + request_url)
    search_results = requests.get(request_url).json()

    if search_results['meta']['code'] == 200:
        if len(search_results['data']):
            return search_results['data'][0]['id']
        else:
            print(error + 'User does not exist!' + endc)
    else:
        print('Error Fetching username')
        return None


def get_name():
    return input("Enter the username of the user: ")


def search_user():
    insta_username = get_name()
    info(name="user", uid=get_user_id(insta_username))
    load_index()


def save_data(posts):
    if posts['meta']['code'] == 200:
        if len(posts['data']):
            # Fetching the most recent media
            image_name = posts['data'][0]['id'] + '.jpeg'
            image_url = posts['data'][0]['images']['standard_resolution']['url']
            urlretrieve(image_url, image_name)
            print(okb + 'Your image has been downloaded in Instabot Dir Folder' + endc)
        else:

            print(error + 'Post does not exist!' + endc)
    else:
        print(okg + 'Status code other than 200 received!' + endc)


def view_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % APP_ACCESS_TOKEN
    print('GET request url : %s' % request_url)
    posts = requests.get(request_url).json()
    save_data(posts)


def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print('GET request url: %s' % request_url)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print(okb + 'There is no recent post of the user!' + endc)
            exit()
    else:
        print('Error')
        exit()


def make_comment():
    name = get_name()
    media_id = get_post_id(name)
    comment_text = input("Enter your comment:")
    print(comment_text)
    request_url = (BASE_URL + "/media/%s/comments") % media_id
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
    post_a_comment = requests.post(request_url, payload).json()
    print('POST request url : %s' % request_url)
    if post_a_comment['meta']['code'] == 200:
        print(okg + "Thanks! Your comment has been posted successfully" + endc)

    else:
        print(error + "Failed! Comment has not been posted.Please try again" + endc)
        exit()


def show_liked_posts():
    request_url = (BASE_URL + 'users/self/media/liked?access_token=%s') % APP_ACCESS_TOKEN
    user_liked = requests.get(request_url).json()
    if user_liked['meta']['code'] == 200:
        if len(user_liked['data']):
            image_name = user_liked['data'][0]['id'] + '.jpeg'
            image_url = user_liked['data'][0]['images']['standard_resolution']['url']
            urlretrieve(image_url, image_name)
            print(okg + "Liked media has been downloaded!\nName: " + image_name + endc)
        else:
            print(error + "Could not find posts" + endc)
    else:
        print(error + 'Error check network settings' + endc)


def delete_neg_comment():
    media_id = get_post_id(get_name())
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print('GET request url : %s' % request_url)
    comment_info = requests.get(request_url).json()
    if comment_info['meta']['code'] == 200:
        for x in range(0, len(comment_info['data'])):
            comment_id = comment_info['data'][x]['id']
            comment_text = comment_info['data'][x]['text']
            # Naive implementation to delete negative comments
            blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
            if blob.sentiment.p_neg > blob.sentiment.p_pos:
                print("It's a negative comment: %s") % comment_text
                delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % APP_ACCESS_TOKEN
                delete_info = requests.delete(delete_url).json()
                if delete_info['meta']['code'] == 200:
                    print(okg + "Comment deleted successfully" + endc)

                else:
                    print(error + "Sorry we couldn't delete this comment! Try Again" + endc)
            else:
                print(okb + "Positive comment" + endc)
    else:
        print(error + "Status code other than 200 received" + endc)


def get_user_post():
    user_id = get_user_id(get_name())
    if user_id is None:
        print(error + 'User does not exist!' + endc)
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print('GET request url : %s' % request_url)
    user_media = requests.get(request_url).json()
    save_data(user_media)


loc = []


def get_location():
    lat = input("Enter latitude coordinate of the location")
    lat = float(lat)
    lon = input("Enter longitude coordinate of the location")
    lon = float(lon)
    request_url = (BASE_URL + 'locations/search?lat=%.2f&lng=%.2f&access_token=%s') % lat, lon, APP_ACCESS_TOKEN
    print(request_url)
    location = requests.get(request_url).json()
    if location['meta']['code'] == 200:
        if len(location['data']):
            for x in range(0, len(location['data'])):
                print(location['data'][x]['id'] + " " + location['data'][x]['name'])
                ids = location['data'][x]['id']
                ids = int(ids)
                loc.append(ids)
            print(loc)
    else:
        print("Meta code other than 200 received")


def natural_calamities():
    get_location()

    tag_name = input("Enter the tag for searching posts")
    if tag_name == "earthquake" or tag_name == "flood" or tag_name == "drought" or tag_name == "landslide" or tag_name == "drought" or tag_name == "cyclone" or tag_name == "tsunami":
        request_url = (BASE_URL + 'tags/%s/media/recent?access_token=%s') % (tag_name, APP_ACCESS_TOKEN)
        print('GET %s') % request_url
        disaster = requests.get(request_url).json()
        # print disaster
        if disaster['meta']['code'] == 200:
            if len(disaster['data']):
                for x in range(0, len(disaster['data'])):
                    print(disaster['data'][x]['location']['id'])
                    print(disaster['data'][x]['location']['name'])
                    loc_id = disaster['data'][x]['location']['id']
                    for x in range(0, len(loc)):
                        if loc_id == loc[x]:
                            print(okg + "Matched! successfully" + endc)
                            for x in range(0, len(disaster['data'])):
                                print(disaster['data'][x]['link'])
                                print(okg + "image found" + endc)
                            break
            else:
                print(error + "image not found" + endc)
        else:
            print(error + "Check net connection" + endc)
    else:
        print(error + "Tags inserted don't match " + endc)


def load_index():
    menu = "\n\n1.View your profile\n2.Search User by username\n3.Get your recent post\n4.Make comment on " \
           "post\n5.Show liked posts of user\n6.Delete negative comment\n7.Get User Post\n8.Information about natural " \
           "calamities\n9.Exit\n "
    ch = input(menu)

    options = {
        1: info,
        2: search_user,
        3: view_post,
        4: make_comment,
        5: show_liked_posts,
        6: delete_neg_comment,
        7: get_user_post,
        8: natural_calamities,
        9: exit
    }
    options[int(ch)]()


if __name__ == '__main__':
    print(okb + "Welcome to InstaBot" + endc)
    import_keys()
    load_index()
    # self_info()
