from flask import Flask, render_template, request
import mistune
from pathlib import Path
import markdown

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("landing_page.html")


@app.route("/blog")
def blog():
    article_name = request.args.get('article_name')
    print("Article: " + article_name)
    with open(Path(__file__).parent / "static" / "blog_articles" / (article_name + ".md"), "r") as article_file:
        article_string = article_file.read()

    article_html = markdown.markdown(article_string, extensions=['fenced_code', 'codehilite'])
    return render_template("blog_article.html", article_html=article_html)


if __name__ == "__main__":
    app.run(debug=True)