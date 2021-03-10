from flask import Flask, render_template, redirect, request, make_response
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
            time = spoti_friends.pretty_date_from_timestamp(i["timestamp"])
            page.append(f"{i['user']['name']} - {i['track']['name']} by {i['track']['artist']['name']}  ({time})")

        resp = make_response("<br>".join(page))

        if expire:
            resp.set_cookie("token", webToken, expires=expire)

        return resp
    else:
        return redirect("/")


@app.route("/howto")
def instructions():
    return """
    1. In Chrome (on computer) open <a href=https://open.spotify.com target="_blank">https://open.spotify.com</a>
     and log in. <br>
    2. Open the Inspector window by pressing Ctrl+Shift+C. <br>
    3. In the opened window, click the Application tab. <br> <img src=static/ins1.png> <br>
    4. Choose Cookies, then https://open.spotify.com <br> <img src=static/ins2.png> <br>
    5. In the sp_dc row click Value two times (marked in green). <br> <img src=static/ins3.png> <br>
    6. Copy the sp_dc token using Ctr+C. <br>
    7. Go back to the <a href="/">main page</a> and paste your token. <br>
    8. The token will be saved automatically in your browser, you will need to change it once a year. <br>
    """


if __name__ == '__main__':
    app.run()
