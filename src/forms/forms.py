from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange, Length


class EditProfileForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Новый пароль")
    confirm_password = PasswordField(
        "Повторите пароль", validators=[EqualTo("password", message="Пароли должны совпадать")]
    )
    submit = SubmitField("Сохранить изменения")


def user_choices():
    from models.models import User
    return User.query


class BoardForm(FlaskForm):
    name = StringField("Название доски", validators=[DataRequired()])
    submit = SubmitField("Создать доску")


class TaskForm(FlaskForm):
    name = StringField("Название", validators=[DataRequired(), Length(max=100)])
    status = StringField("Статус", validators=[DataRequired(), Length(max=100)])
    priority = IntegerField("Приоритет", validators=[DataRequired(), NumberRange(min=1, max=10)])
    description = TextAreaField("Описание", validators=[DataRequired()])
    board_id = SelectField("Номер доски", coerce=int, validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        from models.models import Board

        self.board_id.choices = [(board.id, board.name) for board in Board.query.all()]


class ColumnForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    task_id = IntegerField('Task ID', validators=[DataRequired(), NumberRange(min=1)])


class ContentForm(FlaskForm):
    content = StringField('Содержание', validators=[DataRequired()])
    submit = SubmitField('Добавить')
