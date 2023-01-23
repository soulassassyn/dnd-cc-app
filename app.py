from flask import Flask, request, render_template, session, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from sqlalchemy.orm import sessionmaker
from passlib.hash import sha256_crypt
from dotenv import load_dotenv
from models import User, engine
from wtforms import Form, StringField, validators
import openai
import os
load_dotenv()

app = Flask(__name__)
app.config['TESTING'] = True
app.secret_key = os.getenv('FL_KEY')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
Session = sessionmaker(bind=engine)
session = Session()
# Loads the private API_KEY from a separate file
# If you'd like to use this code you will need your own API Key
# You can generate your own at https://beta.openai.com/
openai.api_key = os.getenv('API_KEY')

# DEBUG Boolean
debug = False

switch_state = not debug

@app.route("/switch", methods=["POST"])
def toggle_switch():
    global switch_state
    switch_state = not switch_state
    print(f"switch state: {switch_state}")
    return "DEBUG API: {}".format("On" if switch_state else "Off")

@app.route("/state")
def get_state():
    return {"DEBUG API:": "On" if switch_state else "Off"}

@login_manager.user_loader
def load_user(user_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        return session.query(User).get(user_id)
    finally:
        session.close()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

class loginForm(Form):
    username = StringField('username', [validators.Length(min=4, max=25)])
    password = StringField('password', [validators.Length(min=8, max=40)])

@app.route('/login', methods=['GET', 'POST'])
def login():
    lform = loginForm(request.form)
    if request.method == 'POST' and lform.validate():
        # Get the user data from the form
        username = lform.username.data
        password = lform.password.data

        # Check the user credentials
        user = session.query(User).filter_by(username=username).first()

        # If the user exists and the password is correct
        if user is not None and sha256_crypt.verify(password, user.password):
            try:
                # Log the user in
                login_user(user, remember=True)
                return redirect(url_for('process_quiz'))
            finally:
                session.close()
        else:
            # Show an error message
            session.close()
            flash('Invalid username or password')
            return redirect(url_for('login'))
    else:
        # Show the login form
        return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

# User registration form validation class
class registrationForm(Form):
    username = StringField('username', [validators.Length(min=4, max=25)])
    email = StringField('email', [validators.Email()])
    password = StringField('password', [validators.Length(min=8, max=40)])

@app.route('/register', methods=['GET', 'POST'])
def register():
    rform = registrationForm(request.form)
    if request.method == 'POST' and rform.validate():
        # Get the user data from the form
        username = rform.username.data
        password = rform.password.data
        email = rform.email.data

        Session = sessionmaker(bind=engine)
        session = Session()

        # Check if the username is already taken
        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user is None:
            # Salt and hash the password
            hashed_password = sha256_crypt.hash(password)
            # Create a new user and add it to the database
            new_user = User(username=username, password=hashed_password, email=email)
            session.add(new_user)
            session.commit()
            return redirect(url_for('login'))
        else:
            # Show an error message
            return 'Username already taken'
    else:
        # Show the register form
        return render_template('register.html')

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    return render_template("dashboard.html")

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
@login_required
def process_quiz():
    races = ["Dragonborn", "Dwarf", "Elf", "Gnome", "Half-Elf", "Halfling", "Half-Orc", "Human", "Tiefling", "Custom..."]
    # racesExtra = ["Aarakocra", "Aasimar", "Air Genasi", "Bugbear", "Centaur", "Changeling", "Deep Gnome", "Duergar", "Earth Genasi", "Eladrin", "Fairy", "Firbolg", "Fire Genasi", "Githyanki", "Githzerai", "Goblin", "Goliath", "Harengon", "Hobgoblin", "Kenku", "Kobold", "Lizardfolk", "Minotaur", "Orc", "Satyr", "Sea Elf", "Shadar-kai", "Shifter", "Tabaxi", "Tortle", "Triton", "Water Genasi", "Yuan-ti"]
    classes = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard", "Custom..."]
    # backgrounds = ["Acolyte", "Criminal/Spy", "Folk Hero", "Noble", "Sage", "Soldier", "Custom..."]

    global debug

    if request.method == "POST":
        # Get the answers to the quiz questions from the first page submission
        q1 = request.form.get("q1")
        q2 = request.form.get("q2")
        q3 = request.form.get("q3")
        q4 = request.form.get("q4")
        q5 = request.form.get("q5")
        q6 = request.form.get("q6")
        charSex = request.form.get("charSex")
        charRace = request.form.get("charRace")
        charClass = request.form.get("charClass")
        charName = request.form.get("charName")
        charRegion = "Faerûn"
        
        # Use the answers to generate a backstory using the ChatGPT API
        if switch_state == True:
            backstory = generate_backstory(q1, q2, q3, q4, q5, q6, charSex, charRace, charClass, charName, charRegion)
        else:
            backstory = "Barriston grew up in a small secluded village, on the edge of the Realm of Davorel. His parents were members of an ancient line of Paladin Knights that had served the realm since its founding. He was raised to be dutiful and respectful, learning from an early age the importance of chivalry and honour. He watched as his village grew more prosperous over the years due to trade with travelers from far and wide. But as it did so, fear began to creep into everyday life--stories of bandits and monsters terrorising local merchants spread like wildfire, until eventually it became too dangerous for traders to enter their borders anymore. With no other options left, Barriston's parents decided to join a group of other villagers who set off together in search for safety elsewhere. They made their way southwards through treacherous terrain until they reached a large city called Sontacia that promised protection within its walls. It was there that Barriston found himself recruited by the local Paladin Order—an organization that dedicated itself solely to protecting those in need against any kind of oppression or threat. For several years he trained under these warriors' tutelage, honing his skills both in combat and diplomacy alike as he learnt what it meant to fight for justice while still remaining fair-minded and diplomatic towards all sides involved in any conflict he found himself embroiled in later on down his path. Now armed with both strength and chastity at his side, Barriston strives each day to make a difference–to protect those who cannot protect themselves; so that others may live without fear just as he once did growing up back home before tragedy struck them all those many years ago when he was yet but just a boy."
        
        # Splits the 'backstory' paragraph in half for easier presentation
        halfbs = int(len(backstory) / 2)
        ccount = 0
        spaceNext = False
        for periods in backstory[halfbs::]:
            ccount += 1
            if spaceNext == True:
                if periods == ' ':
                    break
            if periods == '.':
                spaceNext = True
        halfSentence = halfbs + ccount
        firstHalf = ""
        secondHalf = ""
        for first in backstory[:halfSentence]:
            firstHalf += first
        for second in backstory[halfSentence:]:
            secondHalf += second
        
        return render_template("backstory.html", firstHalf=firstHalf, secondHalf=secondHalf, charName=charName)
    
    return render_template("create01.html", races=races, classes=classes, debug=debug)

def generate_backstory(q1, q2, q3, q4, q5, q6, charSex, charRace, charClass, charName, charRegion):
  # Use the ChatGPT API to generate a backstory based on the quiz answers
    response = openai.Completion.create(
        model="text-davinci-003",
        
        prompt=f"Create a rich backstory for a Dungeons & Dragons character named {charName}. {charSex} is a {charRace} {charClass}. Add a specific town or city from {charRegion} that {charName} is from. Also include explanations for why {charSex} wants {q1}, why they struggle with {q5} and are {q6} towards others. In addition to all of that, make sure the backstory is creative and explains the character's life up to the current day. Write three paragraphs.",
            
        # Max 1,000 requests for $10
        max_tokens=1000,
        top_p=1,
        temperature=0.8,
        frequency_penalty=0.5,
        presence_penalty=0.5
        )
    backstory = response["choices"][0]["text"]
    print(backstory)
    return backstory

@app.route("/pricing", methods=["GET"])
def pricing():
    return render_template("pricing.html")

@app.route("/faq", methods=["GET"])
def faq():
    return render_template("faq.html")

@app.route("/release", methods=["GET"])
def release():
    return render_template("release.html")

# Sends user to the login route if they aren't logged in and try to access a restricted area of the site
@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

@app.route("/test", methods=["GET"])
def test():
    return render_template("test.html")