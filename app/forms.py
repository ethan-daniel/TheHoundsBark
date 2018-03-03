from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class SubmitForm(FlaskForm):
    author = StringField("Name", validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    article = TextAreaField("Article", widget=TextArea(), validators=[DataRequired()])
    type = SelectField("Category", choices=[("", ""), ("Feature", "Feature"), ("Opinion", "Opinion"),
                                            ("Entertainment", "Entertainment"), ("Sports", "Sports"),
                                            ("News", "News"), ("Flipside", "Flipside")], validators=[DataRequired()])
    password = PasswordField("Secret Password", validators=[DataRequired()])
    submit = SubmitField("Submit")