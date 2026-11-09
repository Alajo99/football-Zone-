from flask import Flask, send_from_directory
import os
import requests
from html import escape

app = Flask(__name__)

SPORTMONKS_BASE = "https://api.sportmonks.com/v3/football"


def get_sportmonks_data(endpoint):
    """Request data from Sportmonks and return its JSON response."""
    token = os.getenv("SPORTMONKS_TOKEN")
    if not token:
        raise ValueError("Sportmonks token is missing.")

    response = requests.get(
        f"{SPORTMONKS_BASE}/{endpoint}",
        params={"api_token": token},
        timeout=15
    )
    response.raise_for_status()
    return response.json()


def team_names(match):
    participants = match.get("participants") or []
    names = [
        item.get("name", "Team")
        for item in participants
        if isinstance(item, dict)
    ]
    home = names[0] if names else "Home"
    away = names[1] if len(names) > 1 else "Away"
    return escape(str(home)), escape(str(away))


def score_label(match):
    scores = match.get("scores") or []
    values = []
    for item in scores:
        score = item.get("score") or {}
        if isinstance(score, dict) and score.get("goals") is not None:
            values.append(str(score["goals"]))
    return " - ".join(values) if values else "VS"


@app.route("/sw.js")
def service_worker():
    response = send_from_directory(
        os.path.dirname(os.path.abspath(__file__)),
        "sw.js",
        mimetype="application/javascript"
    )
    response.headers["Service-Worker-Allowed"] = "/"
    return response


@app.route("/manifest.json")
def manifest():
    return send_from_directory(
        os.path.dirname(os.path.abspath(__file__)),
        "manifest.json"
    )


@app.route("/icon-192.png")
def icon192():
    return send_from_directory(
        os.path.dirname(os.path.abspath(__file__)),
        "icon-192.png"
    )


@app.route("/icon-512.png")
def icon512():
    return send_from_directory(
        os.path.dirname(os.path.abspath(__file__)),
        "icon-512.png"
    )


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="manifest" href="/manifest.json">
        <meta name="theme-color" content="#00e676">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Football Zone</title>
        <style>
            * { box-sizing: border-box; }
            body { margin: 0; background: #08111f; color: white;
                   font-family: Arial, sans-serif; }
            header { background: #101e30; padding: 20px; display: flex;
                     justify-content: space-between; align-items: center;
                     border-bottom: 2px solid #00e676; }
            header h1 { margin: 0; color: #00e676; font-size: 23px; }
            .hero { padding: 30px 20px; background: linear-gradient(135deg,
                    #123d32, #101e30); text-align: center; }
            .hero h2 { font-size: 28px; }
            .hero p, .card p { color: #c6d4e1; }
            .button { display: inline-block; background: #00e676;
                      color: #07111d; padding: 12px 22px; border-radius: 25px;
                      text-decoration: none; font-weight: bold; margin-top: 10px; }
            main { padding: 18px; }
            .section-title { color: #00e676; margin-top: 25px; }
            .card { background: #142337; padding: 18px; margin: 14px 0;
                    border-radius: 14px; border: 1px solid #253950; }
            .card h3 { margin-top: 0; }
            nav { display: flex; justify-content: space-around;
                  background: #101e30; padding: 15px 5px;
                  position: sticky; bottom: 0; }
            nav a { color: white; text-decoration: none; font-size: 13px; }
            footer { text-align: center; padding: 20px; color: #8293a7;
                     font-size: 12px; }
        </style>
    </head>
    <body>
        <header><h1>⚽ FOOTBALL ZONE</h1><span>☰</span></header>
        <section class="hero">
            <h2>Your Football World</h2>
            <p>Scores, competitions and the beautiful game — all in one place.</p>
            <a class="button" href="/livescores">⚽ Check Live Scores</a>
        </section>
        <main>
            <h2 class="section-title">🔥 MATCH CENTRE</h2>
            <div class="card">
                <h3>⚽ Follow the Action</h3>
                <p>Check available live football matches.</p>
                <a class="button" href="/livescores">View Matches</a>
            </div>
            <h2 class="section-title">🏆 COMPETITIONS</h2>
            <div class="card">
                <h3>🏆 Football Leagues</h3>
                <p>Explore football competitions.</p>
                <a class="button" href="/leagues">View Leagues</a>
            </div>
            <div class="card">
                <h3>📰 Football News</h3>
                <p>Football news and updates coming soon.</p>
            </div>
        </main>
        <nav>
            <a href="/">🏠 Home</a>
            <a href="/livescores">⚽ Scores</a>
            <a href="/leagues">🏆 Leagues</a>
        </nav>
        <footer>Football Zone © 2026</footer>
        <script>
            if ("serviceWorker" in navigator) {
                navigator.serviceWorker.register("/sw.js");
            }
        </script>
    </body>
    </html>
    """


@app.route("/livescores")
def livescores():
    page = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Live Scores - Football Zone</title>
        <style>
            body { background:#08111f; color:white; font-family:Arial,sans-serif;
                   padding:20px; margin:0; }
            h1 { color:#00e676; }
            .match-card { display:block; background:#142238; color:white;
                          padding:16px; margin:12px 0; border-radius:12px;
                          text-decoration:none; border:1px solid #253950; }
            .match-card:active { background:#1c3450; }
            .teams { font-size:17px; font-weight:bold; }
            .score { color:#00e676; padding:0 8px; }
            .hint { color:#aab9c9; font-size:12px; margin-top:9px; }
            a.back { color:#00e676; }
        </style>
    </head>
    <body>
        <h1>⚽ Live Scores</h1>
        <p>Tap any match to view its details.</p>
    """

    try:
        data = get_sportmonks_data("livescores")
        matches = data.get("data", [])

        if not matches:
            page += "<p>No live matches available right now.</p>"

        for match in matches:
            match_id = match.get("id")
            if not match_id:
                continue

            home, away = team_names(match)
            score = escape(score_label(match))
            state = match.get("state") or {}
            status = escape(str(state.get("name", "Live match")))
            page += f"""
            <a class="match-card" href="/match/{int(match_id)}">
                <div class="teams">{home}
                    <span class="score">{score}</span>{away}
                </div>
                <div class="hint">{status} · Tap to view match details</div>
            </a>
            """

    except ValueError as error:
        page += f"<p>{escape(str(error))}</p>"
    except requests.RequestException:
        page += "<p>Could not connect to Sportmonks. Please try again.</p>"
    except (KeyError, TypeError, ValueError):
        page += "<p>Could not read the match data. Please refresh and try again.</p>"

    page += """
        <p><a class="back" href="/livescores">Refresh Scores</a></p>
        <p><a class="back" href="/">Back to Home</a></p>
    </body>
    </html>
    """
    return page


@app.route("/match/<int:match_id>")
def match_details(match_id):
    page_start = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Match Details - Football Zone</title>
        <style>
            body { background:#08111f; color:white; font-family:Arial,sans-serif;
                   padding:20px; margin:0; }
            h1 { color:#00e676; }
            .box { background:#142238; padding:18px; margin:14px 0;
                   border-radius:12px; }
            .green { color:#00e676; }
            a { color:#00e676; }
        </style>
    </head>
    <body><h1>⚽ Match Details</h1>
    """
    try:
        data = get_sportmonks_data(f"fixtures/{match_id}")
        fixture = data.get("data") or {}
        if not fixture:
            return page_start + """
                <p>Match details are not available.</p>
                <p><a href="/livescores">Back to Live Scores</a></p>
                </body></html>
            """

        home, away = team_names(fixture)
        score = escape(score_label(fixture))
        state = fixture.get("state") or {}
        status = escape(str(state.get("name", "Not available")))
        starting_at = escape(str(fixture.get("starting_at", "Not available")))
        league = fixture.get("league") or {}
        league_name = escape(str(league.get("name", "Not available")))

        return page_start + f"""
            <div class="box">
                <h2>{home} <span class="green">{score}</span> {away}</h2>
                <p><b>Status:</b> {status}</p>
                <p><b>Date:</b> {starting_at}</p>
                <p><b>Competition:</b> {league_name}</p>
            </div>
            <p><a href="/livescores">← Back to Live Scores</a></p>
            <p><a href="/">Home</a></p>
            </body></html>
        """
    except ValueError as error:
        message = escape(str(error))
    except requests.RequestException:
        message = "Could not retrieve this match from Sportmonks."
    return page_start + f"""
        <p>{message}</p>
        <p><a href="/livescores">Back to Live Scores</a></p>
        </body></html>
    """


@app.route("/leagues")
def leagues():
    return """
    <!DOCTYPE html>
    <html>
    <head><meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Leagues - Football Zone</title></head>
    <body style="background:#08111f;color:white;font-family:Arial;padding:20px">
        <h1 style="color:#00e676">🏆 Football Leagues</h1>
        <div style="background:#142337;padding:15px;border-radius:12px">
            <p>🇩🇰 Superliga</p>
            <p>🏴 Premiership</p>
            <p>🏆 Superliga Play-offs</p>
            <p>🏆 Premiership Play-offs</p>
        </div>
        <p><a style="color:#00e676" href="/">Back to Home</a></p>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")), debug=False)
