from flask import Flask, render_template, request
import mistune
from pathlib import Path
import markdown
import csv

app = Flask(__name__)



@app.route("/")
def home():
    recent_articles = list(articles())[-3:]
    examples = read_examples_meta()
    return render_template("landing_page.html", article_names=recent_articles, examples=examples)


@app.route("/aboutme")
def about_me():
    return render_template("about_me.html")


@app.route("/blog/article")
def blog_article():
    article_name = request.args.get('article_name')

    with open(Path(__file__).parent / "static" / "blog_articles" / (article_name), "r") as article_file:
        article_string = article_file.read()

    article_html = markdown.markdown(article_string, extensions=['fenced_code', 'codehilite'])
    return render_template("blog_article.html", article_html=article_html)

@app.route("/examples")
def examples():
    examples = read_examples_meta()
    return render_template("examples.html", examples=examples)


@app.route("/blog")
def blog():
    article_names = articles()
    return render_template("blog_overview.html", article_names=article_names)


def articles():
    article_dir = (Path(__file__).parent / "static" / "blog_articles")

    def split_name(filename: Path):
        release_date, name = filename.name.split("_")
        return release_date, name[:-3].replace("-", " "), filename

    article_names = map(split_name, list(article_dir.iterdir()))
    return article_names


def read_examples_meta():
    with open("resources/projects_meta.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        return list(csvreader)[1:]


if __name__ == "__main__":
    app.run(debug=True)