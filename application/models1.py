from .database import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(50), unique=True, nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True)

    # Relationships
    scores = db.relationship('Score', backref='user', lazy='subquery')
    roles = db.relationship('Role', secondary='user_role', backref='users', lazy='subquery')

    def __repr__(self):
        return f"<User {self.user_email}>"


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), unique=True, nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"<Role {self.name}>"


class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)


class Subject(db.Model):
    __tablename__ = 'subject'
    subject_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    # Chapters under this subject
    chapters = db.relationship('Chapter', backref='subject', lazy='subquery')
    # Quizzes under this subject
    quizzes = db.relationship('Quiz', backref='subject', lazy='subquery')

    def __repr__(self):
        return f"<Subject {self.name}>"


class Chapter(db.Model):
    __tablename__ = 'chapter'
    chapter_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    content_url = db.Column(db.String(255))

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.subject_id'), nullable=False)

    quizzes = db.relationship('Quiz', backref='chapter', lazy='subquery')

    def __repr__(self):
        return f"<Chapter {self.name}>"


class Quiz(db.Model):
    __tablename__ = 'quiz'
    quiz_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    date_quiz = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    duration = db.Column(db.Time, nullable=False)

    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.chapter_id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.subject_id'), nullable=False)

    questions = db.relationship('Question', backref='quiz', lazy='subquery')
    scores = db.relationship('Score', backref='quiz', lazy='subquery')

    def __repr__(self):
        return f"<Quiz {self.name}>"


class Question(db.Model):
    __tablename__ = 'question'
    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String(500), nullable=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255), nullable=False)
    option4 = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)

    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False)

    def __repr__(self):
        return f"<Question {self.question[:30]}...>"


class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.subject_id'), nullable=False)

    score = db.Column(db.Integer, nullable=False)
    total_score = db.Column(db.Integer, nullable=False)
    taken_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Score {self.score}/{self.total_score}>"
