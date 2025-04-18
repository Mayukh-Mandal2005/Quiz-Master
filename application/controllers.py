from flask import Flask, render_template, redirect, request, url_for, session
from flask import current_app as app    # refers to the app object created
from datetime import datetime, timezone, date
from .models import *
import matplotlib.pyplot as plt

@app.route("/")
def home():
    return redirect(url_for("login"))

# Login Route
@app.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        pwd = request.form.get("pwd")
        this_user = User.query.filter_by(username=username).first()
        if this_user:
            if this_user.password == pwd:
                session["username"] = this_user.username
                if this_user.role == "admin":
                    return redirect(url_for("admin_dashboard"))
                else:
                    return redirect(url_for("user_dashboard"))
            else:
                return render_template("incorrect_p.html")
        else:
            return render_template("not_exist.html")

    return render_template("login.html")


# Register Route
@app.route("/register", methods = ["GET","POST"])
def register():
    if request.method == "POST":
        fullname = request.form.get("name")
        qualification = request.form.get("qualification")
        dob = request.form.get("dob")
        username = request.form.get("username")
        pwd = request.form.get("pwd")
        this_user = User.query.filter_by(username = username).first()
        if this_user:
            return render_template("already.html")
        else:
            new_user = User(full_name = fullname, qualification = qualification, dob = dob, username = username, password = pwd)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))

    return render_template("register.html")


# Logout Route
@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username", None)   #Remove the username from the session
    return redirect(url_for("login"))


# User Dashboard Route
@app.route("/user_dashboard")
def user_dashboard():
    if "username" not in session:
        return redirect(url_for("login"))   #Redirect the user if he is not logged in the session

    this_user = User.query.filter_by(username = session["username"]).first()
    if not this_user:
        return redirect(url_for("login"))

    quizzes = Quiz.query.all()
    return render_template("user_dash.html", quizzes = quizzes, full_name = this_user.full_name)


@app.route("/scores")
def scores():
    if "username" not in session:
        return(redirect(url_for("login")))

    this_user = User.query.filter_by(username = session["username"]).first()
    if not this_user:
        return redirect(url_for("login"))

    quizzes = Quiz.query.all()
    scores = Scores.query.filter_by(user_id = this_user.id).all()
    return render_template("scores.html",quizzes = quizzes, scores = scores, full_name = this_user.full_name)


@app.route("/view_quiz/<int:quiz_id>")
def view_quiz(quiz_id):
    if "username" not in session:
        return redirect(url_for("login"))

    this_user = User.query.filter_by(username = session["username"]).first()
    if not this_user:
        return redirect(url_for("login"))

    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return redirect(url_for("user_dashboard"))

    questions = Question.query.filter_by(quiz_id = quiz.id).all()
    return render_template("view_quiz.html", quiz = quiz, questions = questions, full_name = this_user.full_name)


@app.route("/start_quiz/<int:quiz_id>/<int:question_number>", methods = ["GET","POST"])
def start_quiz(quiz_id, question_number = 1):
    if "username" not in session:
        return redirect(url_for("login"))

    this_user = User.query.filter_by(username = session["username"]).first()
    if not this_user:
        return redirect(url_for("login"))

    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return redirect(url_for("user_dashboard"))

    questions = Question.query.filter_by(quiz_id = quiz_id).all()
    total_questions = len(questions)

    if total_questions == 0:
        return(redirect(url_for("user_dashboard")))

    if question_number > total_questions:
        new_score = Scores(
            quiz_id=quiz_id,
            user_id=this_user.id,
            questions=total_questions,
            timestamp = datetime.now(timezone.utc).strftime("%d-%m-%Y %H:%M:%S"),
            score=session.pop("score",0)
        )
        db.session.add(new_score)
        db.session.commit()
        return redirect(url_for("scores"))

    question = questions[question_number - 1]   #Fetches the current question as indexing starts from 0

    if request.method == "POST":
        user_answer = request.form.get("answer")
        if user_answer == str(question.correct):
            session["score"] = session.get("score", 0) + 1

        return(redirect(url_for("start_quiz", quiz_id = quiz_id, question_number = question_number + 1)))

    return render_template("start_quiz.html", quiz = quiz, question = question, total_questions = total_questions, question_number = question_number)


# Admin Dashboard
@app.route("/admin_dashboard")
def admin_dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    this_user = User.query.filter_by(username = session["username"]).first()
    if not this_user or this_user.role != "admin":
        return redirect(url_for("login"))

    subjects = Subject.query.all()
    return render_template("admin_dash.html", subjects = subjects, full_name = this_user.full_name)


@app.route("/users")
def users():
    if "username" not in session:
        return redirect(url_for("login"))

    this_user = User.query.filter_by(username = session["username"]).first()
    if not this_user or this_user.role != "admin":
        return redirect(url_for("login"))

    users = User.query.all()
    return render_template("users.html", users = users, full_name = this_user.full_name)


@app.route("/quiz_management")
def quiz_management():
    if "username" not in session:
        return redirect(url_for("login"))

    this_user = User.query.filter_by(username = session["username"]).first()
    if not this_user or this_user.role != "admin":
        return redirect(url_for("login"))

    chapters = Chapter.query.all()
    quizzes = Quiz.query.all()
    return render_template("quizmanagement.html", chapters = chapters, quizzes = quizzes, full_name = this_user.full_name)


# Subject Management
@app.route("/new_subject", methods = ["GET","POST"])
def new_subject():
    if "username" not in session:
        return redirect(url_for("login"))

    this_user = User.query.filter_by(username = session["username"]).first()
    if not this_user or this_user.role != "admin":
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form.get("name")
        desc = request.form.get("desc")
        new_subject = Subject(name = name, desc = desc)
        db.session.add(new_subject)
        db.session.commit()
        return redirect(url_for("admin_dashboard"))
    return render_template("newsubject.html")


@app.route("/edit_subject/<int:subject_id>", methods = ["GET","POST"])
def edit_subject(subject_id):
    if "username" not in session:
        return redirect(url_for("login"))

    this_user = User.query.filter_by(username = session["username"]).first()
    if not this_user or this_user.role != "admin":
        return redirect(url_for("login"))

    subject = Subject.query.get(subject_id)
    if not subject:
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        name = request.form.get("name")
        desc = request.form.get("desc")
        subject.name = name
        subject.desc = desc
        db.session.commit()
        return redirect(url_for("admin_dashboard"))

    return render_template("newsubject.html", subject = subject)


@app.route("/delete_subject/<int:subject_id>", methods = ["GET","POST"])
def delete_subject(subject_id):
    if "username" not in session:
        return redirect(url_for("login"))

    this_user = User.query.filter_by(username = session["username"]).first()
    if not this_user or this_user.role != "admin":
        return redirect(url_for("login"))

    subject = Subject.query.get(subject_id)
    if subject:
        db.session.delete(subject)
        db.session.commit()
    return redirect(url_for("admin_dashboard"))


# Chapter Management
@app.route("/new_chapter/<int:subject_id>", methods=["GET","POST"])
def new_chapter(subject_id):
    if "username" not in session:
        return redirect(url_for("login"))

    this_user = User.query.filter_by(username = session["username"]).first()
    if not this_user or this_user.role != "admin":
        return redirect(url_for("login"))

    subject = Subject.query.get(subject_id)
    if not subject:
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        name = request.form.get("name")
        desc = request.form.get("desc")
        new_chapter = Chapter(name = name, desc = desc, subject_id = subject_id)
        db.session.add(new_chapter)
        db.session.commit()
        return redirect(url_for("admin_dashboard"))

    return render_template("newchapter.html", subject_id = subject_id)


@app.route("/edit_chapter/<int:chapter_id>", methods = ["GET","POST"])
def edit_chapter(chapter_id):
    if "username" not in session:
        return redirect(url_for("login"))

    this_user = User.query.filter_by(username = session["username"]).first()
    if not this_user or this_user.role != "admin":
        return redirect(url_for("login"))

    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        name = request.form.get("name")
        desc = request.form.get("desc")
        chapter.name = name
        chapter.desc = desc
        db.session.commit()
        return redirect(url_for("admin_dashboard"))

    return render_template("newchapter.html", chapter = chapter, subject_id = chapter.subject_id)


@app.route("/delete_chapter/<int:chapter_id>")
def delete_chapter(chapter_id):
    if "username" not in session:
        return redirect(url_for("login"))

    this_user = User.query.filter_by(username = session["username"]).first()
    if not this_user or this_user.role != "admin":
        return redirect(url_for("login"))

    chapter = Chapter.query.get(chapter_id)
    if chapter:
        db.session.delete(chapter)
        db.session.commit()
    return redirect(url_for("admin_dashboard"))


# Quizzes Management
@app.route("/new_quiz", methods = ["GET","POST"])
def new_quiz():
    if "username" not in session:
        return redirect(url_for("login"))

    this_user = User.query.filter_by(username = session["username"]).first()
    if not this_user or this_user.role != "admin":
        return redirect(url_for("login"))

    chapters = Chapter.query.all()      #Extracting all chapters for the dropdown

    if request.method == "POST":
        chapter_id = request.form.get("chapter_id")
        if not chapter_id:
            return redirect(url_for("quiz_management"))

        name = request.form.get("name")
        quizdate = date.fromisoformat(request.form.get("date"))
        duration = int(request.form.get("duration"))

        new_quiz = Quiz(name = name, quizdate = quizdate, duration = duration, chapter_id = chapter_id)
        db.session.add(new_quiz)
        db.session.commit()
        return redirect(url_for("quiz_management"))

    return render_template("newquiz.html", chapters = chapters)


@app.route("/edit_quiz/<int:quiz_id>", methods = ["GET", "POST"])
def edit_quiz(quiz_id):
    if "username" not in session:
        return redirect(url_for("login"))

    this_user = User.query.filter_by(username=session["username"]).first()
    if not this_user or this_user.role != "admin":
        return redirect(url_for("login"))

    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return redirect(url_for("quiz_management"))

    if request.method == "POST":
        name = request.form.get("name")
        quizdate = date.fromisoformat(request.form.get("date"))
        duration = int(request.form.get("duration"))
        quiz.name = name
        quiz.quizdate = quizdate
        quiz.duration = duration
        db.session.commit()
        return redirect(url_for("quiz_management"))

    return render_template("newquiz.html", quiz = quiz, chapter_id = quiz.chapter_id)


@app.route("/delete_quiz/<int:quiz_id>")
def delete_quiz(quiz_id):
    if "username" not in session:
        return redirect(url_for("login"))

    this_user = User.query.filter_by(username=session["username"]).first()
    if not this_user or this_user.role != "admin":
        return redirect(url_for("login"))

    quiz = Quiz.query.get(quiz_id)
    if quiz:
        db.session.delete(quiz)
        db.session.commit()
    return redirect(url_for("quiz_management"))


# Question management
@app.route("/new_question/<int:quiz_id>", methods = ["GET", "POST"])
def new_question(quiz_id):
    if "username" not in session:
        return redirect(url_for("login"))

    this_user = User.query.filter_by(username = session["username"]).first()
    if not this_user or this_user.role != "admin":
        return redirect(url_for("login"))

    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return redirect(url_for("quiz_management"))

    if request.method == "POST":
        title = request.form.get("title")
        statement = request.form.get("statement")
        option1 = request.form.get("option1")
        option2 = request.form.get("option2")
        option3 = request.form.get("option3")
        option4 = request.form.get("option4")
        correct = request.form.get("correct")

        new_question = Question(title = title, statement = statement, option1 = option1, option2 = option2, option3 = option3, option4 = option4, correct = correct, quiz_id = quiz_id)
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for("quiz_management"))

    return render_template("newquestion.html", quiz = quiz)


@app.route("/edit_question/<int:question_id>", methods = ["GET", "POST"])
def edit_question(question_id):
    if "username" not in session:
        return redirect(url_for("login"))

    this_user = User.query.filter_by(username=session["username"]).first()
    if not this_user or this_user.role != "admin":
        return redirect(url_for("login"))

    question = Question.query.get(question_id)
    if not question:
        return redirect(url_for("quiz_management"))

    if request.method == "POST":
        title = request.form.get("title")
        statement = request.form.get("statement")
        option1 = request.form.get("option1")
        option2 = request.form.get("option2")
        option3 = request.form.get("option3")
        option4 = request.form.get("option4")
        correct = request.form.get("correct")
        question.title = title
        question.statement = statement
        question.option1 = option1
        question.option2 = option2
        question.option3 = option3
        question.option4 = option4
        question.correct = correct
        db.session.commit()
        return redirect(url_for("quiz_management"))

    return render_template("newquestion.html", question = question, quiz_id = question.quiz_id)

@app.route("/delete_question/<int:question_id>")
def delete_question(question_id):
    if "username" not in session:
        return redirect(url_for("login"))

    this_user = User.query.filter_by(username=session["username"]).first()
    if not this_user or this_user.role != "admin":
        return redirect(url_for("login"))

    question = Question.query.get(question_id)
    if question:
        db.session.delete(question)
        db.session.commit()
    return redirect(url_for("quiz_management"))


# Search Functionality
@app.route("/search", methods=["GET"])
def search():
    if "username" not in session:
        return redirect(url_for("login"))

    this_user = User.query.filter_by(username=session["username"]).first()
    if not this_user or this_user.role != "admin":
        return redirect(url_for("login"))

    query = request.args.get("query")
    if not query:
        return redirect(url_for("admin_dashboard"))

    subjects = Subject.query.filter(Subject.name.ilike(f"%{query}%")).all()
    users = User.query.filter(User.username.ilike(f"%{query}%")).all()
    quizzes = Quiz.query.filter(Quiz.name.ilike(f"%{query}%")).all()

    return render_template("search_results.html", subjects = subjects, users = users, quizzes = quizzes, query = query,  full_name = this_user.full_name)


# Admin Summary
@app.route("/admin_summary")
def admin_summary():
    if "username" not in session:
        return redirect(url_for("login"))

    this_user = User.query.filter_by(username=session["username"]).first()
    if not this_user or this_user.role != "admin":
        return redirect(url_for("login"))

    users = User.query.count()
    subjects = Subject.query.count()
    chapters = Chapter.query.count()
    quizzes = Quiz.query.count()
    questions = Question.query.count()
    scores = Scores.query.count()

    # Plotting the overall summary
    labels = ["Users", "Subjects", "Chapters", "Quizzes", "Questions", "Scores"]
    values = [users, subjects, chapters, quizzes, questions, scores]
    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color=["blue", "green", "red", "purple", "orange", "cyan"])
    plt.xlabel("Categories")
    plt.ylabel("Count")
    plt.title("Admin Summary")
    plt.savefig("static/images/admin_summary.png")
    plt.close()

    total_subjects = Subject.query.all()
    total_scores = Scores.query.all()
    subject_names = [subject.name for subject in total_subjects]
    top_scores = []
    for subject in total_subjects:
        subject_scores = []
        for score in total_scores:
            if score.quiz.chapter.subject_id == subject.id:
                subject_scores.append(score.score)
        if subject_scores:
            top_scores.append(max(subject_scores))
        else:
            top_scores.append(0)

    # Bar Chart for top scores
    plt.figure(figsize=(8, 5))
    plt.bar(subject_names, top_scores, color=["skyblue"])
    plt.xlabel("Subjects")
    plt.ylabel("Top Scores")
    plt.title("Top Scores by Subject")
    plt.savefig("static/images/top_scores.png")
    plt.close()

    return render_template("adminsummary.html", full_name = this_user.full_name)


# User Summary
@app.route("/user_summary")
def user_summary():
    if "username" not in session:
        return redirect(url_for("login"))

    this_user = User.query.filter_by(username = session["username"]).first()
    if not this_user:
        return redirect(url_for("login"))

    total_subjects = Subject.query.all()
    total_quizzes = Quiz.query.all()
    total_scores = Scores.query.filter_by(user_id = this_user.id).all()


    # Plotting Bar Chart for Subject Wise no. of quizzes
    quiz_count = {}
    for subject in total_subjects:
        quiz_count[subject.name] = 0
        for quiz in total_quizzes:
            if quiz.chapter.subject_id == subject.id:
                quiz_count[subject.name] += 1
    if total_quizzes:       #Generates bar chart only if there are quizzes
        plt.figure(figsize=(8, 5))
        plt.bar(quiz_count.keys(), quiz_count.values(), color=["lightgreen"])
        plt.xlabel("Subjects")
        plt.ylabel("No. of quizzes")
        plt.title("Subject Wise No. of Quizzes")
        plt.savefig("static/images/subject_summary.png")
        plt.close()

    #Bar Chart for User's Attempts per Subject
    quiz_attempts = Scores.query.filter_by(user_id = this_user.id).all()

    subject_attempts = {}
    for subject in total_subjects:
        subject_attempts[subject.name] = 0

    for attempt in quiz_attempts:
        quiz = Quiz.query.get(attempt.quiz_id)
        if quiz:
            subject_name = quiz.chapter.subject.name
            subject_attempts[subject_name] += 1

    if quiz_attempts:
        plt.figure(figsize=(8, 5))
        plt.bar(subject_attempts.keys(), subject_attempts.values(), color=["royalblue"])
        plt.xlabel("Subjects")
        plt.ylabel("No. of Attempts")
        plt.title("Attempts per Subject")
        plt.savefig("static/images/attempts_summary.png")
        plt.close()

    return render_template("usersummary.html", full_name = this_user.full_name, scores = total_scores, quizzes = total_quizzes)
