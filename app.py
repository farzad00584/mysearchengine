from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# خواندن داده‌ها از فایل
with open("data.txt", "r", encoding="utf-8") as f:
    texts = [line.strip() for line in f.readlines()]

# قالب HTML صفحه
html_template = """ 
<!DOCTYPE html>
<html lang="fa">
<head>
<meta charset="UTF-8">
<title>موتور جستجوی پیشرفته من</title>
<style>
body { font-family: sans-serif; text-align: center; margin-top: 80px; background: #f5f5f5; }
input[type=text] { width: 60%; padding: 12px; border-radius: 8px; border: 1px solid #ccc; }
button { padding: 12px 25px; border-radius: 8px; background: #4285f4; color: white; border: none; cursor: pointer; margin-left: 5px; }
div.result { margin-top: 25px; width: 60%; margin-left: auto; margin-right: auto; text-align: left; background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
p.result-title { font-weight: bold; margin-bottom: 5px; }
</style>
</head>
<body>
<h1>🔍 موتور جستجوی پیشرفته من</h1>
<form method="GET">
<input type="text" name="q" placeholder="دنبال چی می‌گردی؟" value="{{query}}">
<button type="submit">جستجو</button>
</form>
<div class="result">
{% for r in results %}
<p class="result-title">🔹 نتیجه:</p>
<p>{{r}}</p>
<hr>
{% endfor %}
{% if not results and query %}
<p>❌ نتیجه‌ای پیدا نشد.</p>
{% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    query = request.args.get("q", "")
    if query:
        query_words = query.lower().split()
        results = [t for t in texts if all(w in t.lower() for w in query_words)]
    else:
        results = []
    return render_template_string(html_template, results=results, query=query)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
