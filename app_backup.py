from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
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
    </body>
    </html>
    """

@app.route("/livescores")
def livescores():
    return """
    <html>
    <body style="background:#08111f;color:white;font-family:Arial;padding:20px">
    <h1 style="color:#00e676">⚽ Live Scores</h1>
    <p>Open this page to check live matches.</p>
    <p>Live match data will be connected here next.</p>
    <a style="color:#00e676" href="/">Back to Home</a>
    </body>
    </html>
    """

@app.route("/leagues")
def leagues():
    return """
    <html>
    <body style="background:#08111f;color:white;font-family:Arial;padding:20px">
    <h1 style="color:#00e676">🏆 Football Leagues</h1>
    <div style="background:#142337;padding:15px;border-radius:12px">
    <p>🇩🇰 Superliga</p>
    <p>🏴 Premiership</p>
    <p>🏆 Superliga Play-offs</p>
    <p>🏆 Premiership Play-offs</p>
    </div>
    <a style="color:#00e676" href="/">Back to Home</a>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=False)





