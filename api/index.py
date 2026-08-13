import json
import re
from urllib.parse import urlparse
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="../templates")

STORED_EXPORTS = []

IMAGE_EXTS = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg')
VIDEO_EXTS = ('.mp4', '.webm', '.mov', '.m4v', '.mkv')
AUDIO_EXTS = ('.mp3', '.ogg', '.wav', '.flac', '.m4a')
DOC_EXTS = ('.pdf', '.docx', '.txt', '.zip', '.rar', '.7z', '.json', '.csv')

def get_attachment_type(url):
    """Parses URL path and returns attachment category."""
    path = urlparse(url).path.lower()
    if any(path.endswith(ext) for ext in IMAGE_EXTS):
        return "image"
    if any(path.endswith(ext) for ext in VIDEO_EXTS):
        return "video"
    if any(path.endswith(ext) for ext in AUDIO_EXTS):
        return "audio"
    if any(path.endswith(ext) for ext in DOC_EXTS):
        return "doc"
    return "other"

def parse_chat_exporter_json(data):
    guild_name = data.get("guild", {}).get("name", "Direct Messages")
    channel_name = data.get("channel", {}).get("name", "unknown-channel")
    raw_messages = data.get("messages", [])

    parsed_messages = []
    for msg in raw_messages:
        author_info = msg.get("author", {})
        
        raw_attachments = msg.get("attachments", [])
        attachments = []
        
        has_image = False
        has_video = False
        has_audio = False
        has_doc = False

        for att in raw_attachments:
            if isinstance(att, dict) and att.get("url"):
                url = att.get("url")
                att_type = get_attachment_type(url)
                
                if att_type == "image": has_image = True
                elif att_type == "video": has_video = True
                elif att_type == "audio": has_audio = True
                elif att_type == "doc": has_doc = True

                attachments.append({
                    "url": url,
                    "type": att_type
                })

        content = msg.get("content", "")
        has_link = bool(re.search(r'https?://', content))

        # Categorize primary media type
        media_type = "none"
        if has_image: media_type = "image"
        elif has_video: media_type = "video"
        elif has_audio: media_type = "audio"
        elif has_doc: media_type = "doc"

        parsed_messages.append({
            "id": str(msg.get("id", "")),
            # Pass the raw ISO string directly so JS can convert it!
            "iso_timestamp": str(msg.get("timestamp", "")), 
            "guild": guild_name,
            "channel": f"#{channel_name}" if not channel_name.startswith("#") else channel_name,
            "author": author_info.get("nickname") or author_info.get("name") or "Unknown User",
            "avatar": author_info.get("avatarUrl", ""),
            "content": content,
            "attachments": attachments,
            "media_type": media_type,
            "has_image": has_image,
            "has_video": has_video,
            "has_audio": has_audio,
            "has_doc": has_doc,
            "has_link": has_link,
            "has_attachment": len(attachments) > 0
        })
    return parsed_messages

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def index(path):
    global STORED_EXPORTS

    if request.method == 'POST' and 'file' in request.files:
        uploaded_file = request.files['file']
        if uploaded_file and uploaded_file.filename.endswith('.json'):
            try:
                file_data = json.load(uploaded_file)
                STORED_EXPORTS = parse_chat_exporter_json(file_data)
            except Exception as e:
                print(f"Error parsing JSON: {e}")

    return render_template(
        "index.html", 
        logs=STORED_EXPORTS,
        total_count=len(STORED_EXPORTS)
    )

if __name__ == "__main__":
    app.run(debug=True)