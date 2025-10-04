# app.py
from flask import Flask, request, render_template_string, abort, redirect
import os, csv

app = Flask(__name__)

# ---------- خواندن داده‌ها از data.csv ----------
DATA_FILE = "data.csv"

def load_data():
    rows = []
    if not os.path.exists(DATA_FILE):
        return rows
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({
                "id": r.get("id","").strip(),
                "title": r.get("title","").strip(),
                "snippet": r.get("snippet","").strip(),
                "content": r.get("content","").strip(),
                "url": r.get("url","").strip()
            })
    return rows

# ---------- قالب HTML صفحه اصلی ----------
INDEX_HTML = """
<!doctype html>
<html lang="fa">
<head>
<meta charset="utf-8">
<title>Let's go 🔥🚀</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{font-family:Tahoma, sans-serif; background:#f7f7f7; margin:0; padding:0}
.container{max-width:900px;margin:40px auto;padding:0 15px}
.search-box{display:flex; justify-content:center; margin-bottom:25px}
input[type=text]{width:70%;padding:12px;border-radius:24px;border:1px solid #ccc;font-size:16px}
button{padding:12px 18px;border-radius:24px;border:none;background:#1a73e8;color:#fff;margin-left:10px;cursor:pointer}
.results{background:#fff;padding:12px;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.06)}
.item{padding:12px 10px;border-bottom:1px solid #eee}
.item:last-child{border-bottom:none}
.title{font-weight:700;color:#1a0dab;font-size:18px;margin-bottom:6px}
.snippet{color:#444}
a.title-link{text-decoration:none}
.meta{color:#666;font-size:13px;margin-top:8px}
</style>
</head>
<body>
<div class="container">
<h2>🔎 Let's go 🔥🚀</h2>
<form method="GET" class="search-box">
<input type="text" name="q" placeholder="عبارت را وارد کنید..." value="{{query|e}}">
<button type="submit">جستجو</button>
</form>

<div class="results">
{% if not query %}
<p style="padding:12px;color:#555">عبارتی وارد کنید و Enter بزنید یا دکمه جستجو را بزنید.</p>
{% else %}
<p style="padding:8px 12px;color:#333">نتایج برای: <strong>{{query|e}}</strong> — {{results|length}} مورد</p>
{% for r in results %}
<div class="item">
{% if r.url %}
<a class="title-link" href="{{r.url}}" target="_blank" rel="noopener noreferrer"><div class="title">{{r.title}}</div></a>
{% else %}
<a class="title-link" href="/view/{{r.id}}"><div class="title">{{r.title}}</div></a>
{% endif %}
<div class="snippet">{{r.snippet}}</div>
<div class="meta">شناسه: {{r.id}}</div>
</div>
{% endfor %}
{% if results|length == 0 %}
<p style="padding:12px;color:#900">هیچ نتیجه‌ای پیدا نشد.</p>
{% endif %}
{% endif %}
</div>
</div>
</body>
</html>
"""

# ---------- قالب HTML صفحه داخلی ----------
VIEW_HTML = """
<!doctype html>
<html lang="fa">
<head>
<meta charset="utf-8">
<title>{{item.title}} | Let's go 🔥🚀</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{font-family:Tahoma, sans-serif; background:#fafafa; margin:0; padding:0}
.container{max-width:900px;margin:30px auto;padding:0 15px}
.card{background:#fff;padding:20px;border-radius:10px;box-shadow:0 2px 12px rgba(0,0,0,0.06)}
h1{margin-top:0}
.back{display:inline-block;margin-bottom:12px;color:#1a73e8;text-decoration:none}
</style>
</head>
<body>
<div class="container">
<a class="back" href="/">◀ بازگشت به نتایج</a>
<div class="card">
<h1>{{item.title}}</h1>
<p style="color:#555">{{item.content}}</p>
</div>
</div>
</body>
</html>
"""

# ---------- مسیرها ----------
@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "").strip()
    items = load_data()
    results = []
    if query:
        qwords = [w for w in query.lower().split() if w]
        for item in items:
            text = (item["title"] + " " + item["snippet"] + " " + item["content"]).lower()
            score = sum(1 for w in qwords if w in text)
            if score > 0:
                results.append((score, item))
        results.sort(key=lambda x: x[0], reverse=True)
        results = [r[1] for r in results]
    return render_template_string(INDEX_HTML, query=query, results=results)

@app.route("/view/<id>", methods=["GET"])
def view_item(id):
    items = load_data()
    for it in items:
        if it["id"] == id:
            if it.get("url"):
                return redirect(it["url"])
            return render_template_string(VIEW_HTML, item=it)
    abort(404)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
