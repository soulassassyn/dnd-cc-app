from flask import Flask, request, render_template, request
from dotenv import load_dotenv
import openai
import os

app = Flask(__name__)
app.config['TESTING'] = True

# Loads the private API_KEY from a separate file
# If you'd like to use this code you will need your own API Key
# You can generate your own at https://beta.openai.com/
load_dotenv()
openai.api_key = os.environ.get('API_KEY')
switch_state = False

@app.route("/switch", methods=["POST"])
def toggle_switch():
    global switch_state
    switch_state = not switch_state
    print(f"switch state: {switch_state}")
    return "DEBUG API: {}".format("On" if switch_state else "Off")

@app.route("/state")
def get_state():
    return {"DEBUG API:": "On" if switch_state else "Off"}

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
    
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def process_quiz():
    if request.method == "POST":
        # Get the answers to the quiz questions from the form submission
        q1 = request.form.get("q1")
        q2 = request.form.get("q2")
        q3 = request.form.get("q3")
        q4 = request.form.get("q4")
        q5 = request.form.get("q5")
        q6 = request.form.get("q6")
        charRealm = "Faerûn"
        charSex = request.form.get("charSex")
        charRace = request.form.get("charRace")
        charClass = request.form.get("charClass")
        charName = request.form.get("charName")
        
        # Use the answers to generate a backstory using the ChatGPT API
        if switch_state == True:
            backstory = generate_backstory(q1, q2, q3, q4, q5, q6, charRealm, charSex, charRace, charClass, charName)
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
        
        print(f"First Half: {firstHalf}")
        print("---")
        print(f"Second Half: {secondHalf}")
        # Return the two halves of backstory to the user
        return render_template("backstory.html", firstHalf=firstHalf, secondHalf=secondHalf, charName=charName)
    
    return render_template("create.html")

def generate_backstory(q1, q2, q3, q4, q5, q6, charRealm, charSex, charRace, charClass, charName):
  # Use the ChatGPT API to generate a backstory based on the quiz answers
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"""Create a rich background story for a Dungeons & Dragons character.
                    {charSex} is a {charRace} {charClass} named {charName}.
                    {charName} is from somewhere in {charRealm}.
                    The character is motivated by {q1}. 
                    They feel {q2} about authority. 
                    {q3} is how they handle conflict.
                    {q4} is their goal.
                    {q5} are their flaws.
                    {q6} is how they relate to others.""",
        # Max 1,000 requests for $10
        max_tokens=700,
        top_p=1,
        temperature=0.9,
        frequency_penalty=0.8,
        presence_penalty=0.5
        )
    backstory = response["choices"][0]["text"]

    return backstory

@app.route("/pricing", methods=["GET"])
def pricing():
    return render_template("pricing.html")

@app.route("/faq", methods=["GET"])
def faq():
    return render_template("faq.html")

@app.route("/test", methods=["GET"])
def test():
    return render_template("test.html")