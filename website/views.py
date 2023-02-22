# anything that's not related to authentication will be placed in this file

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

# file is a blueprint of our application
views = Blueprint('views', __name__)

# defining a view/route
@views.route('/', methods=["POST", "GET"])
@login_required
def home(): # function will run everytime we go this '/' route
    if request.method == "POST":
        note = request.form.get('note')

        if len(note) < 1:
            flash("Note too short!", category = 'error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash ('Note Added!', category='success')
    
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    noteId = note['noteId']
    note = Note.query.get(noteId)
    # if we found a note
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
           
    return jsonify({})