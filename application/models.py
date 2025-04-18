from .database import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    full_name = db.Column(db.String(),nullable = False)
    qualification = db.Column(db.String(),nullable = False)
    dob = db.Column(db.String(),nullable = False)
    username = db.Column(db.String(), unique=True, nullable = False)
    password = db.Column(db.String(), nullable = False)
    role = db.Column(db.String(), default = "user", nullable = False)

    #Relationship
    scores = db.relationship("Scores", backref = "user", cascade = "all, delete")

class Subject(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(), unique = True, nullable = False)
    desc = db.Column(db.String(), nullable = True)

    # Relationships
    chapters = db.relationship("Chapter", backref="subject", cascade="all, delete")

class Chapter(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(), unique = True, nullable = False)
    desc = db.Column(db.String(), nullable = True)
    subject_id = db.Column(db.Integer(), db.ForeignKey("subject.id"), nullable=False)

    # Relationships
    quizzes = db.relationship("Quiz", backref="chapter", cascade="all, delete")

class Quiz(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(), unique = True, nullable = False)
    quizdate = db.Column(db.Date(),nullable = False)
    duration = db.Column(db.Integer(), nullable = False)
    chapter_id = db.Column(db.Integer(), db.ForeignKey("chapter.id"), nullable = False)

    # Relationships
    questions = db.relationship("Question", backref="quiz", cascade="all, delete")
    scores = db.relationship("Scores", backref = "quiz", cascade = "all, delete")

class Question(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    title = db.Column(db.String(), nullable = False)
    statement = db.Column(db.String(), nullable = False)
    option1 = db.Column(db.String(),nullable = False)
    option2 = db.Column(db.String(),nullable = False)
    option3 = db.Column(db.String(),nullable = False)
    option4 = db.Column(db.String(),nullable = False)
    correct = db.Column(db.Integer(), nullable = False)
    quiz_id = db.Column(db.Integer(), db.ForeignKey("quiz.id"),nullable = False)

class Scores(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    quiz_id = db.Column(db.Integer(), db.ForeignKey("quiz.id"), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"),nullable = False)
    questions = db.Column(db.Integer(),nullable = False)
    timestamp = db.Column(db.String(), nullable = False)
    score = db.Column(db.Integer(),nullable = False)
