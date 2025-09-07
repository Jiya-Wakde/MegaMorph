from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"
UPLOAD_FOLDER = "static/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Delete previous DB if exists
if os.path.exists("registrations.db"):
    os.remove("registrations.db")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///registrations.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# ----------- Models ----------------
class Organiser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    events = db.relationship("Event", backref="organiser", lazy=True)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tagline = db.Column(db.String(200))
    description = db.Column(db.Text)
    participation_type = db.Column(db.String(50))
    entry_fee = db.Column(db.String(20))  # Free or Paid
    amount = db.Column(db.Float)  # optional fee
    team_size = db.Column(db.Integer)  # optional max team size
    reg_start = db.Column(db.DateTime)
    reg_end = db.Column(db.DateTime)
    event_start = db.Column(db.DateTime)
    event_end = db.Column(db.DateTime)
    venue = db.Column(db.String(200))
    organizer_name = db.Column(db.String(100))
    organizer_contact = db.Column(db.String(100))
    poster = db.Column(db.String(200))  # optional
    domain = db.Column(db.String(100))
    notes = db.Column(db.Text)
    organiser_id = db.Column(db.Integer, db.ForeignKey("organiser.id"), nullable=False)


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    college = db.Column(db.String(150), nullable=False)
    year_branch = db.Column(db.String(100))
    event_name = db.Column(db.String(100), nullable=False)
    participation_type = db.Column(db.String(20))
    team_name = db.Column(db.String(100))
    team_leader = db.Column(db.String(100))
    team_size = db.Column(db.Integer)
    member1 = db.Column(db.String(100))
    member2 = db.Column(db.String(100))
    member3 = db.Column(db.String(100))
    member4 = db.Column(db.String(100))
    domain = db.Column(db.String(100))
    submission = db.Column(db.String(200))

    __table_args__ = (
        db.UniqueConstraint('email', 'event_name', name='unique_email_per_event'),
    )


class CulturalHighlight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200), nullable=True)  # store image filename
    year = db.Column(db.String(10), nullable=False)
    link = db.Column(db.String(300), nullable=True)


# ----------- Initialize DB ----------------
# with app.app_context():
#     db.drop_all()
#     db.create_all()
#     highlight = CulturalHighlight(
#         title="Ummag – Garba Night",
#         description="Our grand cultural Garba night where students dress in traditional attire and dance with full "
#                     "energy.",
#         image="Umang.jpg",
#         year="2025",
#         link="https://cumminscollege.edu.in/cultural-events/"
#     )
#     highlight1 = CulturalHighlight(
#         title="Anannya",
#         description="🌸10 night of lights, laughter, and celebration! ✨ A celebration of talent, achievements, and togetherness! 🌟 Join us for an unforgettable evening filled with cultural performances, music, dance, and memories that bring our campus to life. 🎶🎭 ",
#     image = "ananya.jpg",  # upload this inside static/uploads/ or wherever you store images
#     year = "2025",
#     link = "https://cumminscollege.edu.in/cultural-events/"
#     )
#     highlight8 = CulturalHighlight(
#         title="Dahi Handi",
#         description="🌸 A festival of energy, courage, and unity 🙌. Relive the playful spirit of Lord Krishna with music, masti, and Dahi Handi! A tradition that blends devotion with fun and youthful energy. 🎶🔥",
#     image = "dahi-handi.jpg",  # upload this inside static/uploads/ or wherever you store images
#     year = "2025",
#     link = "https://cumminscollege.edu.in/cultural-events/"
#     )
#     highlight9 = CulturalHighlight(
#         title="Diwali –",
#         description="🌸A night of lights, laughter, and celebration! 🪔 A festival of lights, joy, and togetherness! 🌟 Let’s illuminate our A festival of lights, joy, and togetherness! 🌟 Let’s illuminate our campus with diyas, decorations, music, and festive cheer as we celebrate the spirit of Diwali with unity and happiness. 🎉 ",
#     image = "diwali.jpg",  # upload this inside static/uploads/ or wherever you store images
#     year = "2025",
#     link = "https://cumminscollege.edu.in/cultural-events/"
#     )
#     highlight6 = CulturalHighlight(
#         title="Farewell party ",
#         description="An evening of memories, laughter, and emotions. Our campus Celebrate the legacy of our seniors with music, dance, and unforgettable memories as they step into a new chapter of life🌈.",
#     image = "farewell-party.jpg",  # upload this inside static/uploads/ or wherever you store images
#     year = "2025",
#     link = "https://cumminscollege.edu.in/cultural-events/"
#     )
#     highlight7 = CulturalHighlight(
#         title="Flashmob",
#         description="Groove 🎶,Rhythm 🥁,Beat 🎵,Fusion 🌈,Vibe 🎉. 🎶 Get to feel the Vibe! A surprise performance filled with energy, rhythm, and dance that will light up the campus and leave everyone amazed. ✨💃🕺 ",
#     image = "flashmob.jpg",  # upload this inside static/uploads/ or wherever you store images
#     year = "2025",
#     link = "https://cumminscollege.edu.in/cultural-events/"
#     )
#     highlight4 = CulturalHighlight(
#         title="Freshers party",
#         description="Start of a joyful journey. 🎉 A grand welcome to the new beginnings! Our Freshers’ Party is all about fun, music, dance, and bonding — a vibrant evening where seniors and juniors come together to celebrate friendship, talent, and memories. 🌟.",
#     image = "freshers-party.jpg",  # upload this inside static/uploads/ or wherever you store images
#     year = "2025",
#     link = "https://cumminscollege.edu.in/cultural-events/"
#     )
#     highlight5 = CulturalHighlight(
#         title="Ganesh chaturthi",
#         description="🌸 Devotion 🙏:( Faith, Prosperity, Auspiciousness, Celebration). 🌸 Join us in celebrating Ganeshotsav – a festival of devotion, joy, and togetherness! 🙏✨ we welcome Bappa with music, dance, and festive spirit as our campus fills with positivity and blessings. 🌟.",
#     image = "ganesh-charturthi.jpg",  # upload this inside static/uploads/ or wherever you store images
#     year = "2025",
#     link = "https://cumminscollege.edu.in/cultural-events/"
#     )
#     highlight2 = CulturalHighlight(
#         title="Rang De ",
#         description="Day of colors 🌈 Celebrate the festival of colors with music, dance, and endless fun! Join us for a vibrant Holi celebration filled with joy,    togetherness, and festive spirit. Let’s paint the campus in colors of happiness! 🎉.",
#         image="rang-de.jpg",  # upload this inside static/uploads/ or wherever you store images
#         year="2025",
#         link="https://cumminscollege.edu.in/cultural-events/"
#     )
#     highlight3 = CulturalHighlight(
#         title="Sphurti",
#         description="The week of energy Celebrate fitness, fun, and friendship! 🎽 Sphurti is here with thrilling games, spirited rivalries, and memories to last a lifetime",
#         image = "sphurti.jpg",  # upload this inside static/uploads/ or wherever you store images
#     year = "2025",
#     link = "https://cumminscollege.edu.in/cultural-events/"
#     )
#     db.session.add(highlight)
#     db.session.add(highlight1)
#     db.session.add(highlight8)
#     db.session.add(highlight9)
#     db.session.add(highlight6)
#     db.session.add(highlight7)
#     db.session.add(highlight3)
#     db.session.add(highlight2)
#     db.session.add(highlight4)
#     db.session.add(highlight5)
#     db.session.commit()
#
#
# with app.app_context():
#     db.create_all()
#
#     # Create admin organiser
#     admin = Organiser(
#         username="admin",
#         password=generate_password_hash("mypassword123")
#     )
#     db.session.add(admin)
#     db.session.commit()
#
#     # Sample Events
#     event1 = Event(
#         name="Autobot Rally",
#         tagline="Transformers Unite!",
#         description="Join the Autobots in thrilling Cybertron-inspired challenges.",
#         participation_type="Team",
#         entry_fee="Free",
#         team_size=4,
#         reg_start=datetime(2025, 9, 1, 10, 0),
#         reg_end=datetime(2025, 9, 10, 18, 0),
#         event_start=datetime(2025, 9, 12, 9, 0),
#         event_end=datetime(2025, 9, 12, 17, 0),
#         venue="Cybertron Hall",
#         organizer_name="Prof. Optimus Prime",
#         organizer_contact="optimus@cybertron.edu",
#         domain="Robotics",
#         notes="Special prizes for best team",
#         organiser=admin
#     )
#
#     event2 = Event(
#         name="Decepticon Robotics Battle",
#         tagline="Battle for Cybertron!",
#         description="Face the Decepticons in intense robotics combat challenges.",
#         participation_type="Team",
#         entry_fee="Paid",
#         amount=50.0,
#         team_size=3,
#         reg_start=datetime(2025, 9, 5, 10, 0),
#         reg_end=datetime(2025, 9, 15, 18, 0),
#         event_start=datetime(2025, 9, 20, 9, 0),
#         event_end=datetime(2025, 9, 20, 17, 0),
#         venue="Cybertron Arena",
#         organizer_name="Prof. Megatron",
#         organizer_contact="megatron@cybertron.edu",
#         domain="Robotics",
#         notes="Cash prizes for winners",
#         organiser=admin
#     )
#
#     db.session.add_all([event1, event2])
#     db.session.commit()

# ----------- Routes ----------------
@app.route("/")
def home():
    return render_template("index.html", events=Event.query.all())


@app.route("/event/<int:event_id>")
def event_details(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template("event_details.html", event=event)


@app.route("/event/<int:event_id>/register", methods=["GET", "POST"])
def register_for_event(event_id):
    event = Event.query.get_or_404(event_id)

    if request.method == "POST":
        # Check for existing registration
        existing = Participant.query.filter_by(
            email=request.form["email"],
            event_name=event.name
        ).first()

        if existing:
            flash("You are already registered for this event with this email.", "warning")
            return redirect(url_for("event_details", event_id=event.id))

        file = request.files.get("submission")
        filename = None
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))

        participant = Participant(
            name=request.form["Name"],
            email=request.form["email"],
            phone=request.form["phone"],
            college=request.form["college"],
            year_branch=request.form.get("yearBranch"),
            event_name=event.name,
            participation_type=request.form.get("participationType"),
            team_name=request.form.get("teamName"),
            team_leader=request.form.get("teamLeader"),
            team_size=request.form.get("teamSize"),
            member1=request.form.get("member1"),
            member2=request.form.get("member2"),
            member3=request.form.get("member3"),
            member4=request.form.get("member4"),
            domain=request.form.get("domain"),
            submission=filename
        )
        db.session.add(participant)
        db.session.commit()

        return render_template("entry_succes.html")

    return render_template("entry.html", event=event)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        organiser = Organiser.query.filter_by(username=username).first()
        if organiser and check_password_hash(organiser.password, password):
            session["user"] = organiser.username
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html")



@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    organiser = Organiser.query.filter_by(username=session["user"]).first()
    if not organiser:
        flash("Organiser not found. Please log in again.", "danger")
        session.pop("user", None)
        return redirect(url_for("login"))

    events = organiser.events  # this is safe now
    return render_template("dashboard.html", events=events, user=organiser.username)


@app.route("/register_event", methods=["GET", "POST"])
def register_event():
    if "user" not in session:
        return redirect(url_for("login"))

    organiser = Organiser.query.filter_by(username=session["user"]).first()

    if request.method == "POST":
        name = request.form["eventName"]
        tagline = request.form.get("tagline")
        description = request.form.get("description")
        participation_type = request.form.get("participationType")
        entry_fee = request.form.get("entryFee")
        amount = request.form.get("amount") or None
        team_size = request.form.get("teamSize") or None
        reg_start = datetime.fromisoformat(request.form["regStart"])
        reg_end = datetime.fromisoformat(request.form["regEnd"])
        event_start = datetime.fromisoformat(request.form["eventStart"])
        event_end = datetime.fromisoformat(request.form["eventEnd"])
        venue = request.form.get("venue")
        organizer_name = request.form.get("organizer")
        organizer_contact = request.form.get("organizerContact")
        domain = request.form.get("domain")
        notes = request.form.get("notes")

        # ---------- Poster Upload ----------
        poster_file = request.files.get("poster")
        poster_filename = None
        if poster_file and allowed_file(poster_file.filename):
            # Secure filename
            filename = secure_filename(poster_file.filename)
            poster_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            # Ensure upload folder exists
            os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

            # Save poster
            poster_file.save(poster_path)

            # Only store filename in DB (not full path)
            poster_filename = filename

        # ---------- Save Event ----------
        new_event = Event(
            name=name,
            tagline=tagline,
            description=description,
            participation_type=participation_type,
            entry_fee=entry_fee,
            amount=amount,
            team_size=team_size,
            reg_start=reg_start,
            reg_end=reg_end,
            event_start=event_start,
            event_end=event_end,
            venue=venue,
            organizer_name=organizer_name,
            organizer_contact=organizer_contact,
            poster=poster_filename,  # saved poster path
            domain=domain,
            notes=notes,
            organiser_id=organiser.id
        )
        db.session.add(new_event)
        db.session.commit()

        flash("Event registered successfully!", "success")
        return render_template("event-success.html", name=organizer_name, event=new_event.name)

    return render_template("register_event.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully!", "info")
    return redirect(url_for("home"))


@app.route("/delete_event/<int:event_id>", methods=["POST"])
def delete_event(event_id):
    if "user" not in session:
        return redirect(url_for("login"))

    event = Event.query.get_or_404(event_id)

    # Only allow the logged-in organiser to delete their own events
    organiser = Organiser.query.filter_by(username=session["user"]).first()
    if event.organiser_id != organiser.id:
        flash("Unauthorized action!", "danger")
        return redirect(url_for("dashboard"))

    db.session.delete(event)
    db.session.commit()
    flash("Event deleted successfully!", "success")
    return redirect(url_for("dashboard"))


@app.route("/event/<event_name>/participants")
def event_participants(event_name):
    if "user" not in session:
        return redirect(url_for("login"))
    participants = Participant.query.filter_by(event_name=event_name).all()
    return render_template("participants.html", event_name=event_name, participants=participants)


@app.route("/highlights")
def highlights():
    highlights = CulturalHighlight.query.all()
    return render_template("highlights.html", highlights=highlights)


@app.route("/add_highlight", methods=["GET", "POST"])
def add_highlight():
    if "user" not in session:
        redirect(url_for('login'))

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        year = request.form["year"]
        file = request.files["image"]

        filename = None
        if file and file.filename != "":
            filename = file.filename
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        new_highlight = CulturalHighlight(
            title=title, description=description, year=year, image=filename
        )
        db.session.add(new_highlight)
        db.session.commit()
        return redirect(url_for("highlights"))

    return render_template("add_highlight.html")


# ----------- Run ----------------
if __name__ == "__main__":
    app.run(debug=True)
