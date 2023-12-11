from flask import Flask, render_template, request
import mistune
from pathlib import Path
import markdown
import csv
import re
import os
os.environ['FLASK_ENV'] = 'production'


app = Flask(__name__)



@app.route("/")
def home():
    recent_articles = list(articles())[-3:]
    print(recent_articles)
    examples = read_examples_meta()
    return render_template("landing_page.html", article_names=recent_articles, examples=examples)


@app.route("/aboutme")
def about_me():
    return render_template("about_me.html")


def safe_article_path(article_name):
    base_path = Path(__file__).parent / "static" / "blog_articles"
    target_path = base_path / (article_name + ".md")
    # Ensure the target path is within the base_path directory
    return target_path if target_path.resolve().parent == base_path.resolve() else None


@app.route("/blog/article")
def blog_article():
    article_name = request.args.get('article_name')

    safe_path = safe_article_path(article_name)

    try:
        with open(safe_path, "r") as article_file:
            article_string = article_file.read()
    except FileNotFoundError:
        return blog()

    article_html = markdown.markdown(article_string, extensions=['fenced_code', 'codehilite', 'tables', 'mdx_math', 'toc'])
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
        release_date, name = filename.stem.split("_", 1)  # Using stem to exclude the file extension
        return release_date, name.replace("-", " "), filename.stem

    article_names = map(split_name, list(article_dir.iterdir()))
    return article_names


def read_examples_meta():
    with open("resources/projects_meta.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        return list(csvreader)[1:]


if __name__ == "__main__":
    app.run(debug=True)