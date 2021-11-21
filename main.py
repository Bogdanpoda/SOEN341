import sys
sys.path.append('.')

import csv
import json

import psycopg2
import email
#import email_validator
#from flask import Flask, render_template, redirect, url_for, session, flash, jsonify, make_response
#from flask_login import UserMixin, login_user, login_required, logout_user, LoginManager, current_user
#from flask_wtf import FlaskForm

#from wtforms import StringField, TextAreaField, PasswordField, RadioField
#from wtforms.fields.html5 import EmailField
#from wtforms.validators import InputRequired, Email, Length, Regexp, EqualTo

import psycopg2
from flask import Flask, render_template, redirect, session, flash, make_response, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email, Length
from flask_login import UserMixin, login_user, login_required, logout_user, LoginManager

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

mydb = psycopg2.connect(
    host="localhost",
    database="SOEN341",
    user="postgres",
    password="000Poda19996934*")

mycursor = mydb.cursor()


@app.route('/',methods=['GET', 'POST'])
def Base():
    #form = QuestionForm()
    #return render_template('Welcome.html', form=form)
    return searches_form()


@app.route('/Welcome.html', methods=['GET', 'POST'])
def Base2():
    form = QuestionForm()
    return render_template('Welcome.html', form=form)


# REGISTERING FEATURE
# ------------------------------------------
@app.route('/Register.html', methods=['GET', 'POST'])
def register_form():
    form = RegisterForm()
    return render_template('Register.html', form=form)


@app.route('/RegisterSuccess,<name>')
def _register_response(name):
    return render_template('RegisterSuccess.html', name=name)


@app.route('/register', methods=['GET', 'POST'])
def handle_register():
    form3 = RegisterForm()
    form = QuestionForm()

    if form3.is_submitted():
        print("submitted")

    if form3.validate():
        print("valid")

    if form3.validate_on_submit():
        # sql query to retrieve the last row
        mycursor.execute("SELECT User_ID FROM Users WHERE User_id=(SELECT max(User_id) FROM Users);")
        last_user_tuple = mycursor.fetchone()
        # verify if it retrieve a tuple or not
        if last_user_tuple is None:
            form3.User_ID = 1
        else:
            print(last_user_tuple)
            form3.User_ID = last_user_tuple[0] + 1  # add one to the User id of the new User
        # Insert the new entry the sql db
        # sql = "INSERT INTO Users(first_name,last_name,Email_address,Password,User_id) VALUES (%s, %s, %s, %s, %s)"
        # val = (form.User_Name.data, form.User_Name.data, form.Email.data, form.Password.data, form.User_ID)

        sql = "INSERT INTO Users(User_name,Email_address,Password,User_id) VALUES (%s, %s, %s, %s)"
        val = (form3.User_Name.data, form3.Email.data, form3.Password.data, form3.User_ID)

        print(val)
        mycursor.execute(sql, val)
        mydb.commit()
       # return redirect(url_for('_register_response', name=form3.User_Name.data))
        return render_template('RegisterSuccess.html', form=form, name=form3.User_Name.data)
    else:
        return render_template('RegisterFail.html', form3=form3)


class RegisterForm(FlaskForm):
    User_ID = 1
    User_Name = StringField('User_Name', validators=[InputRequired(), Length(4, 64)])
    Email = EmailField('Email', validators=[InputRequired(), Email()])
    Password = PasswordField('Password', validators=[InputRequired(), Length(8, 64)])
    Password2 = PasswordField('Repeat Password', validators=[InputRequired()])


# LOGIN FEATURE
# -------------------------------

@app.route('/Login.html', methods=['GET', 'POST'])
def login_form():
    form = LoginForm()
    return render_template('Login.html', form=form)


@app.route('/LoginSuccess,<name>')
def _login_response(name):
    return render_template('LoginSuccess.html', name=name)


@app.route('/<name>')
def set_name(name):
    session['name'] = name
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def handle_Login():
    form = QuestionForm()
    form2 = LoginForm()
    login_key = False
    password_key = False
    user = User()
    if form2.validate_on_submit():
        print("Okey")
        mycursor.execute("SELECT User_Name,Password,User_ID FROM Users;")
        user_tuples = mycursor.fetchall();
        for i in user_tuples:
            if i[0] == form2.User_Name.data:
                login_key = True
                user.id = i[2]
                user.User_Name = i[0]
            if i[1] == form2.Password.data:
                password_key = True

        # print(password_key)
        # print(login_key)

        if password_key and login_key:
            print("OK")
            login_user(user)  # must be user class
            session['username'] = form2.User_Name.data
           # return redirect(url_for('_login_response', name=form2.User_Name.data, form=form))
            responce = make_response(render_template('LoginSuccess.html', form=form, name=form2.User_Name.data, message=message))
            responce.headers.set('message', 'Logged in')
            return responce


        else:
            print("Fail")
            flash('Incorrect username/password!')
            return render_template('LoginFail.html', form=form)
    else:
        return render_template('LoginFail.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    u = User()
    u.id = int(user_id)
    mycursor.execute("SELECT User_Name,User_ID FROM Users;")
    user_tuples = mycursor.fetchall();

    for i in user_tuples:
        if i[1] == u.id:
            u.User_Name = i[0]

    return u


class LoginForm(FlaskForm):
    User_Name = StringField('User_Name', validators=[InputRequired(), Length(4, 64)])
    Password = PasswordField('Password', validators=[InputRequired(), Length(8, 64)])


class User(UserMixin):
    id = 1
    User_Name = ""

    def get(self):
        return self.id


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session['username'] = ""
    return redirect('/')


# Ask a question Feature
# -----------------------
@app.route('/Ask_a_Question.html', methods=['GET', 'POST'])
def question_form():
    # if session['username'] == "":
    # return render_template('Ask_a_Question_Not_logged_in.html')
    # else:
    form = QuestionForm()
    return render_template('Ask_a_Question.html', form=form)


@app.route('/QuestionSuccess')
def _question_response():
    return render_template('QuestionSuccess.html')


@app.route('/question', methods=['GET', 'POST'])
def handle_Question():
    form = QuestionForm()
    if session['username'] == "":
        return render_template('Ask_a_Question_Not_logged_in.html')

    if form.is_submitted():
        print("submitted")

    if form.validate():
        print("valid")

    if form.validate_on_submit():
        # sql query to retrieve the last row
        mycursor.execute(
            "SELECT Question_ID FROM Questions WHERE Question_ID=(SELECT max(Question_ID) FROM Questions);")
        last_question_tuple = mycursor.fetchone()
        # verify if it retrieve a tuple or not
        if last_question_tuple is None:
            form.Question_ID = 1
        else:
            print(last_question_tuple)
            form.Question_ID = last_question_tuple[0] + 1  # add one to the User id of the new User
        # Insert the new entry the sql db
        # sql = "INSERT INTO Questions(Question_ID,Content) VALUES (%s, %s)"
        # val = (form.Question_ID, form.Question.data)
        sql = "INSERT INTO Questions(Question_ID,Content,User_Name,Label) VALUES (%s, %s, %s, %s)"
        val = (form.Question_ID, form.Question.data, session['username'], form.Label.data)
        print(val)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('QuestionSuccess.html', form=form)
    else:
        return render_template('QuestionFail.html', form=form)


class QuestionForm(FlaskForm):
    Question_ID = 1
    Question = StringField('Question',validators=[InputRequired(), Length(4, 1064)])
    Label = StringField('Label')


# Search questions feature
# ------------------------



@app.route('/SearchQuestions.html', methods=['GET', 'POST'])
def searches_form():
    mycursor.execute("SELECT Question_ID,Content,Label,User_name FROM Questions")
    questions = mycursor.fetchall()
    form2=questions
    form3=GetQuestionForm()
    form=QuestionForm()
    return render_template('SearchQuestions.html', form=form, form2=json.dumps(form2), form3=form3,  len=len(questions))


#Display a specific question

@app.route('/getQuestion',methods=['GET','POST'])
def handle_getQuestion():
    form3 = GetQuestionForm()
    if form3.is_submitted():
        print ("submitted")

    if form3.validate():
        print ("valid")

    mycursor.execute("SELECT User_Name,Question_ID,Content,Number_Of_Up_Votes, Number_Of_Down_Votes,Favorite_Answer_ID FROM Questions")

    questions = mycursor.fetchall()
    if form3.Question_ID.data:


        #gettting the right questions from the db
        right_question = questions[int(form3.Question_ID.data)-1]
        session['Question_ID']=right_question[1]
        #get all the answers to the question from the db
        sql = "SELECT Answers.User_Name, Answers.Content, Answers.Answer_ID " \
              "FROM Question_has_Answers, Answers " \
              "WHERE Answers.Answer_ID = Question_has_Answers.Answer_ID  and Question_has_Answers.Question_ID = %s"
        val = (form3.Question_ID.data,)
        mycursor.execute(sql, val)
        answers=mycursor.fetchall()
        print (answers)

        return render_template('DisplayQuestion.html', form=form3,question=right_question, answers=answers, len=len(answers))
    else:
        mycursor.execute("SELECT User_Name,Question_ID,Content FROM Questions")
        questions = mycursor.fetchall()
        return render_template('SearchQuestionsFail.html', form=form3, questions=questions,len=len(questions))


class GetQuestionForm(FlaskForm):
    # Question_ID = RadioField("Question_ID")
    Question_ID = StringField('Question_ID',validators=[InputRequired(), Length(1, 1064)])

# Answering a question

class AnswerForm(FlaskForm):
    Answer_ID = 1
    Answer = StringField("Answer")

@app.route('/answer', methods=['GET', 'POST'])
def handle_Answer():
    if session['username'] == "":
        return render_template('Ask_a_Question_Not_logged_in.html')
    form = AnswerForm()
    if form.is_submitted():
        print("submitted")

    if form.validate():
         print("valid")

    if form.validate_on_submit():
        # UPDATING THE ANSWER ID and its content

         # sql query to retrieve the last row
        mycursor.execute(
            "SELECT Answer_ID FROM Answers WHERE Answer_ID=(SELECT max(Answer_ID) FROM Answers);")
        last_answer_tuple = mycursor.fetchone()
         # verify if it retrieve a tuple or not
        if last_answer_tuple is None:
            form.Answer_ID = 1
        else:
            print (last_answer_tuple)
            form.Answer_ID = last_answer_tuple[0] + 1  # add one to the User id of the new User
        sql = "INSERT INTO Answers(User_Name,Answer_ID,Content) VALUES (%s,%s,%s)"
        val = (session["username"], form.Answer_ID, form.Answer.data)
        mycursor.execute(sql, val)
        mydb.commit()

        # UPDATING THE Question_Has_Answer
        sql = "INSERT INTO Question_has_Answers(Question_ID,Answer_ID) VALUES(%s,%s)"
        val = (session['Question_ID'], form.Answer_ID)
        mycursor.execute(sql, val)
        mydb.commit()

        flash('Answer posted successfully')
        return render_template('Welcome.html', form=form)
    else:
        flash('Invalid answer')
        return render_template('Welcome.html', form=form)

        # UpVotes or DownVotes
        # --------------

class voteQuestion(FlaskForm):
    Vote = RadioField('Vote')

@app.route('/vote', methods=['GET', 'POST'])
def handle_vote():
    if session['username'] == "":
        return render_template('Ask_a_Question_Not_logged_in.html')
    form = voteQuestion()
    if form.is_submitted():
            print("submitted")
    print(form.Vote.data)
    if form.validate():
        print("valid")

    if form.Vote.data:
        mycursor.execute("SELECT * FROM VOTE")
        allvotes = mycursor.fetchall()

        # Verify if the user has already voted for the question
        for i in allvotes:
            if i[0] == session['username'] and i[1] == int(session["Question_ID"]):
                return render_template('AlreadyVoted.html')

        # Adding the vote into the vote table
        val = (session['username'], session['Question_ID'], form.Vote.data)
        sql = "INSERT INTO VOTE VALUES(%s,%s,%s)"
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('SuccesfulVote.html', form=form)
    else:
        return render_template('Welcome.html', form=form)

            # Choosing Favorite Answer
            # -----------------------


class favoriteAnswer(FlaskForm):
    Favorite_Answer = RadioField('Favorite_Answer')

@app.route('/favoriteAnswer', methods=['GET', 'POST'])
def handle_favorite_answer():
    form = favoriteAnswer()
    if form.is_submitted():
        print("submitted")
    print(form.Favorite_Answer.data)
    if form.Favorite_Answer.data:

        # Updating the question favorite answer variable
        val = (int(form.Favorite_Answer.data), session['Question_ID'])
        sql = "Update Questions set Favorite_Answer_ID=%s WHERE Questions.Question_ID=%s  "
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('SuccesfulVote.html', form=form)
    else:
        return render_template('Welcome.html', form=form)


if __name__ == '__main__':
    app.run()
