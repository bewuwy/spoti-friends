from flask import Flask, render_template, redirect, request, make_response
from datetime import datetime
import spoti_friends


app = Flask(__name__)


@app.route("/")
def index():
    if request.cookies.get("sp_dc") is None:
        return render_template("index.html")
    else:
        return redirect("/activity")


@app.route("/activity")
def activity():
    spDc = request.cookies.get("sp_dc")
    if spDc is not None:
        webToken = request.cookies.get("token")
        expire = None
        if webToken is None:
            token = spoti_friends.get_token(spDc)

            # if sp_dc is wrong
            if token is None:
                resp = make_response(redirect("/"))

                resp.set_cookie("sp_dc", "", expires=0)
                return resp
            else:
                webToken = token["accessToken"]
                expire = int(token["accessTokenExpirationTimestampMs"] / 1000)

        friendsActivity = spoti_friends.get_friends_activity(webToken)
        page = []

        for i in friendsActivity:
            time = datetime.fromtimestamp(int(i['timestamp'] / 1000))
            page.append(f"{i['user']['name']} - {i['track']['name']} by {i['track']['artist']['name']}  ({time})")

        resp = make_response("<br>".join(page))

        if expire:
            resp.set_cookie("token", webToken, expires=expire)

        return resp
    else:
        return redirect("/")


@app.route("/instrukcja")
def instrukcja():
    return """
    1. Na komputerze w Chrome wejdź na <a href=https://open.spotify.com target="_blank">https://open.spotify.com</a>
     i zaloguj się <br>
    2. kliknij Ctrl+Shift+C <br>
    3. Otworzy ci sie z prawej strony takie okienko, wybierz zakladke Application <br> <img src=static/ins1.png> <br>
    4. Kliknij w Cookies, a potem w https://open.spotify.com <br> <img src=static/ins2.png> <br>
    5. W kolumnie sp_dc kliknij dwa razy value (zaznaczone na zielono) <br> <img src=static/ins3.png> <br>
    6. Kliknij Ctr+C, masz teraz w schowku swój klucz sp_dc <br>
    7. Wróć na <a href="/">stronę główną</a> i wklej swój klucz <br>
    """


if __name__ == '__main__':
    app.run()
