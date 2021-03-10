import requests
from datetime import datetime, timedelta


def get_token(sp_dc):
    # get authorization token
    url = "https://open.spotify.com/get_access_token?reason=transport&productType=web_player"
    cookies = {"sp_dc": sp_dc}

    response = requests.get(url, cookies=cookies, allow_redirects=False)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_friends_activity(web_token):
    # get friend activity
    url = "https://guc-spclient.spotify.com/presence-view/v1/buddylist"
    headers = {"authorization": f"Bearer {web_token}"}

    response = requests.get(url, headers=headers)

    return response.json()["friends"]


def pretty_date_from_timestamp(ms):
    date = datetime.fromtimestamp(int(ms/1000))
    now = datetime.now()

    delta = now - date
    minute = str(date.minute)
    if len(minute) == 1:
        minute = "0" + minute
    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    if delta <= timedelta(seconds=300):
        return "now"
    elif delta < timedelta(days=2):
        if date.day == now.day:
            return f"today at {date.hour}:{minute}"
        else:
            return f"yesterday at {date.hour}:{minute}"
    elif delta <= timedelta(days=7):
        return f"{weekdays[date.weekday()]} at {date.hour}:{minute}"
    else:
        return f"{delta.days} days ago"


if __name__ == '__main__':
    spDc = "AQA-Gp4aHFyRGAwrn3pfD8Fj7y7-vWolKZLc03HGj5tImufAjq_8bPGkm9Ez2V_ybXb_geU8jWL9ynm2fwovHXe3Iv8mbYSoK8XwXhabAA"

    token = get_token(spDc)
    print(token, end="\n"*2)
    token = token["accessToken"]

    friend_activity = get_friends_activity(token)
    print(friend_activity, end="\n"*2)

    for i in friend_activity:
        time = datetime.fromtimestamp(int(i['timestamp']/1000))
        print(f"{i['user']['name']} - {i['track']['name']} by {i['track']['artist']['name']}  ({time})")
