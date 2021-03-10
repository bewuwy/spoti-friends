from flask import Flask, render_template, redirect, request, make_response
from flask_mobility import Mobility
import spoti_friends

app = Flask(__name__)
Mobility(app)


@app.route("/")
def index():
    e = request.args.get("e")
    if request.cookies.get("sp_dc") is None or e is not None:
        errors = {"noSp_dc": "There is no sp_dc token saved",
                  "wrongSp_dc": "You entered a wrong sp_dc token"}
        if e is None or e not in errors:
            return render_template("index.html")
        else:
            return render_template("index.html", error=errors[e])
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
                resp = make_response(redirect("/?e=wrongSp_dc"))

                resp.set_cookie("sp_dc", "", expires=0)
                return resp
            else:
                webToken = token["accessToken"]
                expire = int(token["accessTokenExpirationTimestampMs"] / 1000)

        friendsActivity = spoti_friends.get_friends_activity(webToken)
        al = []

        for i in friendsActivity:
            time = spoti_friends.pretty_date_from_timestamp(i["timestamp"])
            if i["track"]["context"]["uri"].find("playlist") > -1:
                context_type = "🎵"
            else:
                context_type = "💿"

            trackUrl = "https://open.spotify.com/track/" + i['track']['uri'].split(":")[2]
            artistUrl = "https://open.spotify.com/artist/" + i['track']['artist']['uri'].split(":")[2]
            albumUrl = "https://open.spotify.com/album/" + i['track']['album']['uri'].split(":")[2]
            if len(i['track']['context']['uri'].split(":")) > 3:
                contextUrl = "https://open.spotify.com/" + i['track']['context']['uri'].split(":")[3] + "/" + \
                             i['track']['context']['uri'].split(":")[4]
            else:
                contextUrl = "https://open.spotify.com/" + i['track']['context']['uri'].split(":")[1] + "/" + \
                             i['track']['context']['uri'].split(":")[2]

            al.insert(0, [i['user']['name'], [i['track']['name'], trackUrl], [i['track']['artist']['name'], artistUrl],
                          time, [i['track']['album']['name'], albumUrl], [i['track']['context']['name'], contextUrl],
                          context_type, i["user"].get("imageUrl")])

        resp = make_response(render_template("activity.html", activityList=al))

        if expire:
            resp.set_cookie("token", webToken, expires=expire)

        return resp
    else:
        return redirect("/?e=noSp_dc")


@app.route("/howto")
def instructions():
    return render_template("howto.html")


if __name__ == '__main__':
    app.run(host="192.168.72.203")
