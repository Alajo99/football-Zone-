from flask import Flask, send_from_directory
import os

app = Flask(__name__)
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
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "manifest.json")

@app.route("/icon-192.png")
def icon192():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "icon-192.png")

@app.route("/icon-512.png")
def icon512():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "icon-512.png")

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html><link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#00e676">
    <head>
        <title>Football Zone</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { box-sizing: border-box; }
            body {
                margin: 0;
                background: #08111f;
                color: white;
                font-family: Arial, sans-serif;
            }
            header {
                background: #101e30;
                padding: 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 2px solid #00e676;
            }
            header h1 {
                margin: 0;
                color: #00e676;
                font-size: 23px;
            }
            .hero {
                padding: 30px 20px;
                background: linear-gradient(135deg, #123d32, #101e30);
                text-align: center;
            }
            .hero h2 { font-size: 28px; }
            .hero p { color: #c6d4e1; }
            .button {
                display: inline-block;
                background: #00e676;
                color: #07111d;
                padding: 12px 22px;
                border-radius: 25px;
                text-decoration: none;
                font-weight: bold;
                margin-top: 10px;
            }
            main { padding: 18px; }
            .section-title {
                color: #00e676;
                margin-top: 25px;
            }
            .card {
                background: #142337;
                padding: 18px;
                margin: 14px 0;
                border-radius: 14px;
                border: 1px solid #253950;
            }
            .card h3 { margin-top: 0; }
            .card p { color: #c6d4e1; }
            .tag {
                color: #00e676;
                font-size: 12px;
                font-weight: bold;
            }
            nav {
                display: flex;
                justify-content: space-around;
                background: #101e30;
                padding: 15px 5px;
                position: sticky;
                bottom: 0;
            }
            nav a {
                color: white;
                text-decoration: none;
                font-size: 13px;
            }
            footer {
                text-align: center;
                padding: 20px;
                color: #8293a7;
                font-size: 12px;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>⚽ FOOTBALL ZONE</h1>
            <span>☰</span>
        </header>

        <section class="hero">
            <h2>Your Football World</h2>
            <p>Scores, competitions and the beautiful game — all in one place.</p>
            <a class="button" href="/livescores">⚽ Check Live Scores</a>
        </section>

        <main>
            <h2 class="section-title">🔥 MATCH CENTRE</h2>
            <div class="card">
                <span class="tag">LIVE SCORES</span>
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
</script></body>
    </html>
    """

@app.route("/livescores")
def livescores():
    import os
    import requests
    from html import escape

    token = os.getenv("SPORTMONKS_TOKEN")
    page = """
    <html>
    <head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
    <body style="background:#08111f;color:white;font-family:Arial;padding:20px">
    <h1 style="color:#00e676">⚽ Live Scores</h1>
    """

    if not token:
        return page + '<p>Sportmonks token is missing.</p><a href="/">Back Home</a></body></html>'

    try:
        r = requests.get(
            "https://api.sportmonks.com/v3/football/livescores",
            params={"api_token": token},
            timeout=5
        )
        r.raise_for_status()
        matches = r.json().get("data", [])

        if not matches:
            page += "<p>No live matches available right now.</p>"

        for match in matches:
            names = [
                item.get("name", "Team")
                for item in match.get("participants", [])
            ]
            home = escape(names[0]) if names else "Home"
            away = escape(names[1]) if len(names) > 1 else "Away"

            scores = match.get("scores") or []
            score_text = "VS"
            if scores:
                values = []
                for item in scores:
                    score = item.get("score") or {}
                    if isinstance(score, dict) and score.get("goals") is not None:
                        values.append(str(score["goals"]))
                if values:
                    score_text = " - ".join(values)

            match_id = match.get("id", "")
            page += f'<a href="/match/{match_id}" style="display:block;text-decoration:none;color:white;background:#142238;padding:15px;margin:12px 0;border-radius:12px">{home} <b style="color:#00e676">{score_text}</b> {away}<br><small style="color:#00e676">Tap to view match details →</small></a>'

    except requests.RequestException:
        page += "<p>Could not connect to Sportmonks. Please try again.</p>"

    page += '<p><a style="color:#00e676" href="/livescores">Refresh Scores</a></p><a style="color:#00e676" href="/">Back to Home</a></body></html>'
    return page




@app.route("/match/<int:match_id>")
def match_details(match_id):
    import os
    import requests
    from html import escape

    token = os.getenv("SPORTMONKS_TOKEN")
    if not token:
        return "Sportmonks token is missing", 500

    try:
        r = requests.get(
            f"https://api.sportmonks.com/v3/football/fixtures/{match_id}",
            params={
                "api_token": token,
                "include": "participants;scores;league"
            },
            timeout=10
        )
        r.raise_for_status()
        match = r.json().get("data")

        if not match:
            return "Match details are unavailable.", 404

        names = [
            escape(team.get("name", "Team"))
            for team in match.get("participants", [])
        ]
        home = names[0] if names else "Home"
        away = names[1] if len(names) > 1 else "Away"

        scores = match.get("scores") or []
        score_text = "VS"
        values = []
        for item in scores:
            score = item.get("score") or {}
            if isinstance(score, dict) and score.get("goals") is not None:
                values.append(str(score["goals"]))
        if values:
            score_text = " - ".join(values)

        status = escape(str(match.get("state", {}).get("name", "Unavailable")))

        return f"""
        <html>
        <head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
        <body style="background:#08111f;color:white;font-family:Arial;padding:20px">
        <h1 style="color:#00e676">⚽ Match Details</h1>
        <div style="background:#142238;padding:20px;border-radius:12px;text-align:center">
        <h2>{home}</h2>
        <h1 style="color:#00e676">{score_text}</h1>
        <h2>{away}</h2>
        <p>Status: {status}</p>
        </div>
        <p><a style="color:#00e676" href="/livescores">← Back to Live Scores</a></p>
        <p><a style="color:#00e676" href="/">Home</a></p>
        </body></html>
        """
    except requests.RequestException:
        return "Could not retrieve match details. Please try again.", 502

@app.route("/leagues")
def leagues():
    return """
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Football Leagues - Football Zone</title>
    </head>
    <body style="background:#08111f;color:white;font-family:Arial;padding:20px">
    <h1 style="color:#00e676">🏆 Football Leagues</h1>

    <div style="background:#142337;padding:15px;border-radius:12px">

    <h3>🏴 England</h3>
    <p>⚽ Premier League</p>
    <p>🏆 Championship</p>

    <h3>🇪🇸 Spain</h3>
    <p>⚽ La Liga</p>

    <h3>🇮🇹 Italy</h3>
    <p>⚽ Serie A</p>

    <h3>🇩🇪 Germany</h3>
    <p>⚽ Bundesliga</p>

    <h3>🇫🇷 France</h3>
    <p>⚽ Ligue 1</p>

    <h3>🇪🇺 European Competitions</h3>
    <p>🏆 UEFA Champions League</p>
    <p>🏆 UEFA Europa League</p>
    <p>🏆 UEFA Conference League</p>

    <h3>🇳🇬 Nigeria</h3>
    <p>⚽ Nigeria Premier Football League</p>

    <h3>🇩🇰 Denmark</h3>
    <p>⚽ Superliga</p>

    <h3>🏴 Scotland</h3>
    <p>⚽ Premiership</p>

    </div>

    <br>
    <a style="color:#00e676" href="/">Back to Home</a>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=False)
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=False)





