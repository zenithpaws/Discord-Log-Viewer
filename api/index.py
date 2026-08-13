from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder="../templates")

MOCK_LOGS = [
    {
        "id": "1",
        "timestamp": "2026-08-10 14:22:10",
        "channel": "#general",
        "author": "KiroFox#0001",
        "content": "Hey Aster! Are we building something cool today? :3"
    },
    {
        "id": "2",
        "timestamp": "2026-08-11 09:15:43",
        "channel": "#dev-chat",
        "author": "Aster#1337",
        "content": "Deploying the new Flask backend to Vercel!"
    }
]

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    query = request.args.get("q", "").lower()
    channel_filter = request.args.get("channel", "all")

    filtered_logs = MOCK_LOGS

    if channel_filter != "all":
        filtered_logs = [log for log in filtered_logs if log["channel"] == channel_filter]

    if query:
        filtered_logs = [
            log for log in filtered_logs 
            if query in log["content"].lower() or query in log["author"].lower()
        ]

    return render_template("index.html", logs=filtered_logs, query=query, channel_filter=channel_filter)

if __name__ == "__main__":
    app.run(debug=True)
