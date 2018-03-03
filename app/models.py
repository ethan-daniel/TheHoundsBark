from app import db
from datetime import datetime


class Article:
    def __init__(self, form):
        self.author = form.author.data
        self.title = form.title.data
        self.article = form.article.data
        self.type = form.type.data
