
from flask import Flask, request, redirect, render_template_string, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOADS = "uploads"
os.makedirs(UPLOADS, exist_ok=True)
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")

PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MOMINOV MUSIC</title>
<style>
body {
  background:#11111b; color:white; font-family:Arial;
  padding:20px; max-width:600px; margin:auto;
}
h1 {color:#cba6f7;text-align:center;}
.song {background:#242438;padding:12px;margin:12px 0;border-radius:12px;}
audio {width:100%;}
input,button {margin:8px 0;padding:12px;max-width:100%;}
button {background:#cba6f7;border:0;border-radius:8px;}
</style>
</head>
<body>
<h1>🎵 MOMINOV MUSIC</h1>
<h2>Qo‘shiqlar</h2>
{% for song in songs %}
<div class="song">
<p>{{ song }}</p>
<audio controls preload="none" src="/uploads/{{ song }}"></audio>
</div>
{% else %}
<p>Hozircha qo‘shiqlar yo‘q.</p>
{% endfor %}
<hr>
<h2>Admin — qo‘shiq yuklash</h2>
<form method="post" action="/upload" enctype="multipart/form-data">
<input name="password" type="password" placeholder="Admin paroli" required>
<br>
<input name="song" type="file" accept=".mp3,.wav,.ogg,.m4a" required>
<br>
<button type="submit">🎵 Qo‘shiq yuklash</button>
</form>
<p>{{ message }}</p>
</body>
</html>
"""

@app.route("/")
def home():
    songs = sorted(os.listdir(UPLOADS))
    return render_template_string(PAGE, songs=songs, message="")

@app.route("/upload", methods=["POST"])
def upload():
    if request.form.get("password") != ADMIN_PASSWORD:
        return render_template_string(
            PAGE, songs=sorted(os.listdir(UPLOADS)),
            message="Parol noto‘g‘ri!"
        ), 403

    file = request.files.get("song")
    if not file or not file.filename:
        return "Qo‘shiq tanlanmadi", 400

    filename = secure_filename(file.filename)
    if not filename.lower().endswith((".mp3", ".wav", ".ogg", ".m4a")):
        return "Faqat audio fayllar yuklash mumkin.", 400

    file.save(os.path.join(UPLOADS, filename))
    return redirect("/")

@app.route("/uploads/<path:filename>")
def audio(filename):
    return send_from_directory(UPLOADS, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

