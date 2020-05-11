import math
import random
import string

from flask import Flask, render_template, request, redirect, url_for, flash, session
import bcrypt
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import sqlite3

from sqlalchemy import ForeignKey

app = Flask(__name__)
app.secret_key = 'personalproject'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/site.db'
app.config['DEBUG'] = False
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'jef.anhduc@gmail.com'
app.config['MAIL_PASSWORD'] = 'hzcntmmmyovpwumg'
app.config['MAIL_DEFAULT_SENDER'] = 'PRPROGRAM@PRPROGRAM.com'
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False
mail = Mail()
mail.init_app(app)
db = SQLAlchemy(app)


class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))


class ProgramData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), default="null")
    name = db.Column(db.String(50), default="null")
    pr = db.Column(db.Integer, default=0)
    reps1 = db.Column(db.Integer, default=0)
    percent1 = db.Column(db.Integer, default=0)
    reps2 = db.Column(db.Integer, default=0)
    percent2 = db.Column(db.Integer, default=0)
    reps3 = db.Column(db.Integer, default=0)
    percent3 = db.Column(db.Integer, default=0)
    reps4 = db.Column(db.Integer, default=0)
    percent4 = db.Column(db.Integer, default=0)
    reps5 = db.Column(db.Integer, default=0)
    percent5 = db.Column(db.Integer, default=0)
    reps6 = db.Column(db.Integer, default=0)
    percent6 = db.Column(db.Integer, default=0)
    reps7 = db.Column(db.Integer, default=0)
    percent7 = db.Column(db.Integer, default=0)
    reps8 = db.Column(db.Integer, default=0)
    percent8 = db.Column(db.Integer, default=0)
    reps9 = db.Column(db.Integer, default=0)
    percent9 = db.Column(db.Integer, default=0)
    reps10 = db.Column(db.Integer, default=0)
    percent10 = db.Column(db.Integer, default=0)
    reps11 = db.Column(db.Integer, default=0)
    percent11 = db.Column(db.Integer, default=0)
    reps12 = db.Column(db.Integer, default=0)
    percent12 = db.Column(db.Integer, default=0)
    reps13 = db.Column(db.Integer, default=0)
    percent13 = db.Column(db.Integer, default=0)
    reps14 = db.Column(db.Integer, default=0)
    percent14 = db.Column(db.Integer, default=0)
    reps15 = db.Column(db.Integer, default=0)
    percent15 = db.Column(db.Integer, default=0)
    reps16 = db.Column(db.Integer, default=0)
    percent16 = db.Column(db.Integer, default=0)
    reps17 = db.Column(db.Integer, default=0)
    percent17 = db.Column(db.Integer, default=0)
    reps18 = db.Column(db.Integer, default=0)
    percent18 = db.Column(db.Integer, default=0)
    reps19 = db.Column(db.Integer, default=0)
    percent19 = db.Column(db.Integer, default=0)
    reps20 = db.Column(db.Integer, default=0)
    percent20 = db.Column(db.Integer, default=0)


class User(UserMixin):
    def __init__(self, username, password=None):
        self.id = username
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    user = find_user(user_id)
    if user:
        user.password = None
    return user


def find_user(username):
    connection = sqlite3.connect('data/site.db')
    cur = connection.cursor()
    for row in cur.execute("SELECT username, password from user_data"):
        if not row:
            continue
        if username == row[0]:
            return User(row[0], row[1])
    return None


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == "POST":
        users = find_user(request.form["username"])
        if ' ' in request.form["username"]:
            flash("Please put a single word for your username !")
            return redirect(url_for('register'))
        if not users:
            salt = bcrypt.gensalt()
            encodePassword = bcrypt.hashpw(request.form["password"].encode(), salt)
            userData = UserData(username=request.form["username"], password=encodePassword)
            db.session.add(userData)
            db.session.commit()
            user = find_user(request.form["username"])
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('This username already exists, please select another one')
    else:
        redirect(url_for('register'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == "POST":
        user = find_user(request.form["username"])
        if user and bcrypt.checkpw(request.form["password"].encode(), user.password):
            login_user(user)
            next_page = session.get('next', '/')
            session['next'] = '/'
            return redirect(next_page)
        flash('Wrong username/password. Please try again.')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == "POST":
        id = current_user.id
        nameProgram = request.form['programName']
        prProgram = request.form['PR']
        sets = int(request.form['numberSet'])
        reps = [0] * 20
        percent = [0] * 20
        for x in range(sets):
            repName = 'reps[' + str(x + 1) + ']'
            reps[x] = request.form[repName]
            percentName = 'percent[' + str(x + 1) + ']'
            percent[x] = request.form[percentName]
        programData = ProgramData(username=id, name=nameProgram, pr=prProgram, reps1=reps[0], reps2=reps[1],
                                  reps3=reps[2], reps4=reps[3], reps5=reps[4],
                                  reps6=reps[5], reps7=reps[6], reps8=reps[7], reps9=reps[8], reps10=reps[9],
                                  reps11=reps[10], reps12=reps[11], reps13=reps[12],
                                  reps14=reps[13], reps15=reps[14], reps16=reps[15], reps17=reps[16], reps18=reps[17],
                                  reps19=reps[18], reps20=reps[19],
                                  percent1=percent[0], percent2=percent[1], percent3=percent[2], percent4=percent[3],
                                  percent5=percent[4], percent6=percent[5],
                                  percent7=percent[6], percent8=percent[7], percent9=percent[8], percent10=percent[9],
                                  percent11=percent[10], percent12=percent[11],
                                  percent13=percent[12], percent14=percent[13], percent15=percent[14],
                                  percent16=percent[15], percent17=percent[16], percent18=percent[17],
                                  percent19=percent[18], percent20=percent[19])
        db.session.add(programData)
        db.session.commit()
        flash("Program created ! You can view your program in your Programs !")
        return redirect(url_for('create'))
    return render_template('create.html')


@app.route('/programs', methods=['GET', 'POST'])
@login_required
def programs():
    programName = []
    programNumber = 0
    num = 0
    connection = sqlite3.connect('data/site.db')
    cur = connection.cursor()
    for row in cur.execute('SELECT username, name FROM program_data'):
        if row[0] == current_user.id:
            programName.append(row[1])
            programNumber = programNumber + 1
    if request.method == "POST":
        value = request.form
        for x in range(programNumber):
            if (str(value) == """ImmutableMultiDict([('delete""" + str(x) + """', 'Delete')])"""):
                for row in cur.execute('SELECT name FROM program_data'):
                    if programName[x] == row[0]:
                        deleteStatement = "DELETE from program_data where name = '%s'" % programName[x]
                        cur.execute(deleteStatement)
                        connection.commit()
                        flash('You have deleted the program')
                        return redirect(url_for('programs'))
    return render_template('program.html', data=programName, number=programNumber)


@app.route('/view/<name>')
@login_required
def view(name):
    connection = sqlite3.connect('data/site.db')
    cur = connection.cursor()
    programInfo = []
    programSets = []
    setsRepsPr = []
    percent = []
    plates = []
    barbell = 45
    jumpStart = 0
    jumpEnd = 2
    weight = []
    for row in cur.execute('SELECT * FROM program_data'):
        if row[2] == name:
            programData = row
    for x in programData:
        if x != 0:
            programInfo.append(x)
            programSets.append(x)
    numberPrPercent = 0
    numberSets = 0
    for p in range(4):
        programSets.remove(programSets[0])
    for j in programSets:
        numberPrPercent = numberPrPercent + 1
        numberSets = int(numberPrPercent / 2)
    if len(programSets) != 2:
        for x in range(numberSets):
            setsRepsPr.append(programSets[jumpStart:jumpEnd])
            jumpStart = jumpStart + 2
            jumpEnd = jumpEnd + 2
            if jumpEnd == len(programSets):
                setsRepsPr.append(programSets[jumpStart:])
        for x in range(1, len(programSets), 2):
            percent.append(programSets[x])
    else:
        setsRepsPr.append(programSets)
        percent.append(programSets[1])
    for x in range(numberSets):
        PR = programData[3]
        weightRow = (percent[x] / 100) * PR
        weightRow = round(weightRow, 2)
        weight.append(weightRow)
        numberPlates45 = 0
        numberPlates35 = 0
        numberPlates25 = 0
        numberPlates10 = 0
        numberPlates5 = 0
        numberPlates2p5 = 0
        str45 = ""
        str35 = ""
        str25 = ""
        str10 = ""
        str5 = ""
        str2p5 = ""
        if (weightRow - barbell > 0):
            weightSide = (weightRow - barbell) / 2
            if weightSide / 45 >= 1:
                numberPlates45 = math.floor(weightSide / 45)
                weightSide = weightSide - (numberPlates45 * 45)
                str45 = "+" + str(numberPlates45) + "x45"
            if weightSide / 35 >= 1:
                numberPlates35 = math.floor(weightSide / 35)
                weightSide = weightSide - (numberPlates35 * 35)
                str35 = "+" + str(numberPlates35) + "x35"
            if weightSide / 25 >= 1:
                numberPlates25 = math.floor(weightSide / 25)
                weightSide = weightSide - (numberPlates25 * 25)
                str25 = "+" + str(numberPlates25) + "x25"
            if weightSide / 10 >= 1:
                numberPlates10 = math.floor(weightSide / 10)
                weightSide = weightSide - (numberPlates10 * 10)
                str10 = "+" + str(numberPlates10) + "x10"
            if weightSide / 5 >= 1:
                numberPlates5 = math.floor(weightSide / 5)
                weightSide = weightSide - (numberPlates5 * 5)
                str5 = "+" + str(numberPlates5) + "x5"
            if weightSide / 2.5 >= 1:
                numberPlates2p5 = math.floor(weightSide / 2.5)
                weightSide = weightSide - (numberPlates2p5 * 2.5)
                str2p5 = "+" + str(numberPlates2p5) + "x2.5"
            platesRow = "BB" + str45 + str35 + str25 + str10 + str5 + str2p5
            plates.append(platesRow)
        else:
            plates.append("You can't even lift the barbell")
    return render_template('view.html', name=name, data=programInfo, setNumber=numberSets, setProgram=programSets,
                           rowRepsPr=setsRepsPr, weightData=weight, platesData=plates)


@app.route('/modifyPR/<name>', methods=['GET', 'POST'])
@login_required
def modifyPR(name):
    if request.method == "POST":
        connection = sqlite3.connect('data/site.db')
        cur = connection.cursor()
        for row in cur.execute('SELECT name, pr FROM program_data'):
            if row[0] == name:
                updatePR = int(request.form['modifyPR'])
                cur.execute("Update program_data set pr=? where name=?", (updatePR, name))
                connection.commit()
                flash("Your PR has been updated !")
                return redirect(url_for('home'))
    return render_template('modifyPR.html', name=name)

@app.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changePassword():
    if request.method == "POST":
        connection = sqlite3.connect('data/site.db')
        cur = connection.cursor()
        for row in cur.execute("SELECT username, password from user_data"):
            if(current_user.id == row[0]):
                presentPasswordEnc = row[1]
                currentFormPassword = request.form['currentPassword']
                if bcrypt.checkpw(currentFormPassword.encode(), presentPasswordEnc):
                    id = current_user.id
                    salt = bcrypt.gensalt()
                    newPassword = request.form['newPassword']
                    newPasswordEncoded = bcrypt.hashpw(newPassword.encode(), salt)
                    cur.execute("Update user_data set password=? where username=?", (newPasswordEncoded, id))
                    connection.commit()
                    flash("Your password has been modified !")
                else:
                    flash("Wrong Password")
    return render_template('changepassword.html')

def generateRandomPassword(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


@app.route('/forgotPassword', methods=['GET','POST'])
def forgotPassword():
    if request.method == "POST":
        connection = sqlite3.connect('data/site.db')
        cur = connection.cursor()
        for row in cur.execute("SELECT username, password from user_data"):
            if request.form['emailForm'] == row[0]:
                flash("A new password has been sent to your email, you can change it back after !")
                resetPassword = generateRandomPassword()
                salt = bcrypt.gensalt()
                encodeResetPassword = bcrypt.hashpw(resetPassword.encode(), salt)
                username = request.form['emailForm']
                cur.execute("Update user_data set password=? where username=?", (encodeResetPassword, username))
                connection.commit()
                recipient = username
                msg = Message('Forgot Password from PRProgram', recipients=[recipient])
                msg.body = "Your password has been reset. Your new password is now : "+resetPassword+"\nYou can change your password with it."
                mail.send(msg)
                return redirect(url_for('login'))
        flash("There is no account associated with that email.")
    return render_template('forgotPassword.html')

if __name__ == '__main__':
    app.run()
