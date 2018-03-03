from flask import render_template, flash, redirect, Flask, request, url_for
from werkzeug.utils import secure_filename
from app import app
from .forms import SubmitForm
from datetime import datetime
import glob
import os
import pickle
import config

ALLOWED_EXTENSIONS = set(['png', 'jpeg', 'jpg'])
image_path = ''


@app.route('/')
@app.route('/index')
def index():
    recent_list = get_latest_articles('app/Submitted_Articles/**/**/*.txt')
    feature_list = get_latest_articles('app/Submitted_Articles/**/Feature/*.txt')
    opinion_list = get_latest_articles('app/Submitted_Articles/**/Opinion/*.txt')
    entertainment_list = get_latest_articles('app/Submitted_Articles/**/Entertainment/*.txt')
    sports_list = get_latest_articles('app/Submitted_Articles/**/Sports/*.txt')
    news_list = get_latest_articles('app/Submitted_Articles/**/News/*.txt')
    flipside_list = get_latest_articles('app/Submitted_Articles/**/Flipside/*.txt')

    return render_template('index.html', title='Home', recent_list=recent_list, feature_list=feature_list,
                           opinion_list=opinion_list, entertainment_list=entertainment_list, sports_list=sports_list,
                           news_list=news_list, flipside_list=flipside_list)


def get_latest_articles(pathname):
    article_list = glob.glob(pathname)
    sorted_article_list = sorted(article_list, key=os.path.getctime, reverse=True)
    unpickled_list = []
    for i in range(6):
        unpickled_list.append(pickle.load(open(sorted_article_list[i], "rb")))
    return unpickled_list


@app.route('/feature')
def feature():
    return render_template('feature.html', title='Feature')


@app.route('/opinion')
def opinion():
    return render_template('opinion.html', title='Opinion')


@app.route('/entertainment')
def entertainment():
    return render_template('entertainment.html', title='Entertainment')


@app.route('/sports')
def sports():
    return render_template('sports.html', title='Sports')


@app.route('/news')
def news():
    return render_template('news.html', title='News')


@app.route('/flipside')
def flipside():
    return render_template('flipside.html', title='Flipside')


@app.route('/staff')
def staff():
    return render_template('staff.html', title='Staff')


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = SubmitForm()
    if form.validate_on_submit():
        article_date_path = os.path.join('Submitted_Articles', datetime.now().isoformat()[:7])
        article_date_path_local = os.path.join(config.ROOT_PATH, article_date_path)

        image_date_path = os.path.join('static', 'img', 'Submitted_Images', datetime.now().isoformat()[:7])
        image_date_path_local = os.path.join(config.ROOT_PATH, image_date_path)

        if not os.path.exists(article_date_path_local):
            os.mkdir(article_date_path_local)
        if not os.path.exists(image_date_path_local):
            os.mkdir(image_date_path_local)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if not os.path.exists(os.path.join(article_date_path_local, form.type.data)):
            os.mkdir(os.path.join(article_date_path_local, form.type.data))
        if not os.path.exists(os.path.join(image_date_path_local, form.type.data)):
            os.mkdir(os.path.join(image_date_path_local, form.type.data))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(image_date_path_local, form.type.data))
            image_path_online = "../" + os.path.join(image_date_path, form.type.data, form.title.data + filename[-4:]).replace("\\", "/")
        article_data = {"title": form.title.data, "image_path": image_path_online,"author": form.author.data, "body": form.article.data,
                        "type": form.type.data, "date": datetime.today().strftime('%B %d')}
        article_path_local = os.path.join(article_date_path_local, form.type.data, form.title.data + ".txt")
        pickle.dump(article_data, open(article_path_local, 'wb'), 0)
        return redirect('/')
    return render_template('submit.html',
                           title='Submit Article',
                           form=form)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/login')
# def login():
#    return render_template('login.html', title='Login')


# @app.route('/authorized')
# def authorized():
#   pass
