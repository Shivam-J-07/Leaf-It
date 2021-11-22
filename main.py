####################################################################
###############          Import packages         ###################
####################################################################
from flask import Blueprint, render_template, flash, request
# Import for Migrations
from flask_migrate import Migrate, current
from flask.helpers import url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from __init__ import create_app, db
from models import Plant
from moisture_readings import moisture_levels, last_watered
import os
####################################################################
# our main blueprint
main = Blueprint('main', __name__)

####################################################################
@main.route('/') # home page that return 'index'
def index():
    return render_template("index.html")

####################################################################
@main.route('/profile', methods=['GET']) # profile page that return 'profile'
@login_required
def profile():
    # update moisture and last_watered data
    last_watered()
    moisture_levels()

    plant = Plant.query.filter_by(user_id=current_user.id).first()
    moisture_level = plant.moisture_level
    last_watered_value = plant.last_watered.strftime("%d/%m/%Y %H:%M:%S")

    # get plant image
    try:
        user_file = open(f"static/user_info/user_{current_user.id}", "r").readlines()
        set_profile = user_file[0].split(":")[1]
        
        if set_profile[0] == "T":
            print("set_profile")
            image = url_for('static', filename=f"plant_images/plant_{current_user.id}") 
        else:
            print("placeholder")
            image = url_for('static', filename=f"lightbulb.png")

    except:
        user_file = open(f"static/user_info/user_{current_user.id}", "w+")
        user_file.write("set_profile:False\n")
        print("created")
        image = url_for('static', filename=f"lightbulb.png")
        #user_file.save(os.path.join("./static/user_info", f"user_{current_user.id}"))

    #image = url_for('static', filename=f"plant_images/plant_{current_user.id}")
    # get audio files for user
    audio = url_for('static', filename=f"audio/plant_{current_user.id}.wav")
    #recordings = [audio]

    return render_template('plant_status.html', name=current_user.name, moisture_level=moisture_level, last_watered=last_watered_value, image=image, audio=audio)

@main.route('/profile', methods=['POST'])
def upload_file():
    # plant image
    try:
        image = request.files['image_file']
        if image.filename != '':
            image.save(os.path.join("./static/plant_images", f"plant_{current_user.id}"))
            user_file = open(f"user_{current_user.id}", "w+")
            user_file.write("set_profile:True\n")
            user_file.close()
    except:
        pass
    
    # audio
    try:
        audio = request.files['audio_file']
        audio.save(os.path.join("./static/audio", f"plant_{current_user.id}.wav"))
    except:
        pass

    return redirect(url_for('main.profile'))

####################################################################
@main.route('/new-user', methods=['GET', 'POST']) # page for new users to select plant type
def new_user():
    if request.method == "POST":
        user_id = current_user.id
        plant = Plant(user_id = user_id, plant_type=request.values.get("plant_type"))
        db.session.add(plant)
        db.session.commit()
        flash('Record was successfully added')
        return redirect(url_for('main.profile'))
    print("here")
    return render_template('new_user.html')

####################################################################
app = create_app() # we initialize our flask app using the            
                   #__init__.py function
####################################################################
if __name__ == '__main__':
    db.create_all(app = create_app()) # create the SQLite database
    app.run(debug=True) # run the flask app on debug mode

# Settings for migrations
migrate = Migrate(app, db)