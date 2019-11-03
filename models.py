#!/usr/bin/python3
# models.py

from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import( TimedJSONWebSignatureSerializer as Serializer,
    BadSignature, SignatureExpired)

# system user class
class SystemAdmin(db.Model,UserMixin):
    """This class defines the schema for the university db"""

    # fields definition
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), nullable=False)
    hash_password = db.Column(db.String(128), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)    

    # constructor
    def __init__(self, fullname, username, password):
        self.fullname = fullname
        self.username = username
        self.hash_password = generate_password_hash(password, method='sha256')


# University Class


class University(db.Model):
    """This class defines the schema for the university db"""

    # fields definition
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    location = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    website = db.Column(db.Text, nullable=True)
    telephone = db.Column(db.Integer, nullable=True)
    address = db.Column(db.String(64), nullable=False)
    about = db.Column(db.Text, nullable=True)
    chancellor_name =  db.Column(db.String(64), nullable=False)
    # admin_username = db.Column(db.String(64), nullable=False)
    # admin_password = db.Column(db.String(128), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    faculty = db.relationship('Faculty', backref='university', lazy=True)

    # constructor
    def __init__(self, name, location, email, telephone, address, about,
                chancellor_name):
        self.name = name
        self.location = location
        self.email = email
        self.telephone = telephone
        self.address = address
        self.about = about
        self.chancellor_name = chancellor_name
        # self.admin_username = admin_username
        # self.admin_password = generate_password_hash(admin_password, method='sha256')

    # create a method here to save the cover_letter, phone number, username
    # later on

    # verify the hashed password
    def check_password(self, password):
        """This function verifys if the hashed_password
        matches the password that is passed as an argument and return the
        truthiness"""
        return check_password_hash(self.password_hash, password)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            # 'address': self.address,
            # 'phone': self.phone,
            # 'joined on': self.joined_date
        }

# Faculty Class


class Faculty(db.Model):
    """It defines the schema for a faculty."""


    # fields definition
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    head_of_faculty = db.Column(db.String(64), nullable=False)
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'),
        nullable=False)
    course_id = db.relationship('Course', backref='faculty', lazy=True)
    student_id = db.relationship('Student', backref='faculty', lazy=True)

    # constructor
    def __init__(self, name, head_of_faculty, university,):
        self.name = name
        self.head_of_faculty = head_of_faculty
        self.university = university

# Course Class


class Course(db.Model):
    """It defines the schema for a course."""


    # fields definition
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    duration = db.Column(db.String(7), nullable=False)
    head_of_faculty = db.Column(db.String(64), nullable=False)
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'),
        nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'),
        nullable=False)
    module_code = db.relationship('Module', backref='course', lazy=True)
    student_id = db.relationship('Student', backref='course', lazy=True)

    # constructor
    def __init__(self, name, head_of_faculty, university_id, faculty_id):
        self.name = name
        self.head_of_faculty = head_of_faculty
        self.university_id = university_id
        self.faculty_id = faculty_id


# Module Class


class Module(db.Model):
    """It defines the schema for a module."""


    # fields definition
    id = db.Column(db.Integer, primary_key=True)
    module_code = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    credit_hours = db.Column(db.String(10), nullable=False)
    coordinator = db.Column(db.String(64), nullable=False)
    module_type = db.Column(db.String(10), nullable=False)
    head_of_faculty = db.Column(db.String(64), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'),
        nullable=False)
    student_id = db.relationship('Student', backref='module', lazy=True)

    # constructor
    def __init__(self, name, head_of_faculty, university_id, faculty_id):
        self.name = name
        self.head_of_faculty = head_of_faculty
        self.university_id = university_id
        self.faculty_id = faculty_id


# Student Class
class Student(db.Model,UserMixin):
    """Student model schema"""

    # fields definition
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, unique=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    other_names = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(64), unique=True, index=False)
    phone = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(64), nullable=False)
    date_of_birth = db.Column(db.Text, nullable=False)
    place_of_birth = db.Column(db.Text, nullable=False)
    nationality = db.Column(db.String(100), nullable=False)
    sponsorship = db.Column(db.Text, nullable=False)
    current_year = db.Column(db.Integer, nullable=False)
    current_semester = db.Column(db.Integer, nullable=False)
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'),
        nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'),
        nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'),
        nullable=False)


    # constructor
    def __init__(self, student_id, first_name, last_name, other_names, email, phone,
                address, date_of_birth, place_of_birth, nationality,
                sponsorship, current_year, current_semester, university_id,
                course_id, module_id):
        self.first_name = first_name
        self.last_name = last_name
        self.other_names = other_names
        self.email = email
        self.phone = phone
        self.address = address
        self.date_of_birth = date_of_birth
        self.place_of_birth = place_of_birth
        self.nationality = nationality
        self.sponsorship = sponsorship
        self.current_year = current_year
        self.current_semester = current_semester
        self.university_id = university_id
        self.course_id = course_id
        self.module_id = module_id
        # self.password_hash = generate_password_hash(password)

    # verify the hashed password
    def check_password(self, password):
        """This function verifys if the hashed_password
        matches the password that is passed as an argument and return the
        truthiness"""
        return check_password_hash(self.password_hash, password)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'admin': self.first_name + ' ' + self.last_name,
            'jobTitle': self.jobtitle,
            'email': self.email,
            'company_name': self.company_name,
            'address': self.address,
            'phone': self.phone,
            'bio': self.bio,
            'joined_on': self.joined_date
        }


# Application Class

class Application(db.Model):
    """It defines the schema for a module."""


    # fields definition
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    other_names = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(64), unique=True, index=False)
    phone = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(64), nullable=False)
    date_of_birth = db.Column(db.Text, nullable=False)
    place_of_birth = db.Column(db.Text, nullable=False)
    nationality = db.Column(db.String(100), nullable=False)
    sponsorship = db.Column(db.Text, nullable=False)
    academic_year = db.Column(db.String(10), nullable=False)
    result = db.Column(db.String(100), nullable=False)
    scratch_number = db.Column(db.String(100), nullable=False)
    fee_payment_receipt = db.Column(db.String(100), nullable=False)
    application_date = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'),
        nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'),
        nullable=False)
    receipt_no = db.relationship('ApplicationFee', backref='application', lazy=True)

    


    def __init__(self, first_name, last_name, other_names, email, phone,
                address, date_of_birth, place_of_birth, nationality,
                sponsorship, academic_year, result, scratch_number,
                fee_paymeny_receipt, university_id, course_id):
        self.first_name = first_name
        self.last_name = last_name
        self.other_names = other_names
        self.email = email
        self.phone = phone
        self.address = address
        self.date_of_birth = date_of_birth
        self.place_of_birth = place_of_birth
        self.nationality = nationality
        self.sponsorship = sponsorship
        self.academic_year = academic_year
        self.result = result
        self.scratch_number = scratch_number
        self.fee_paymeny_receipt = fee_paymeny_receipt
        self.university_id = university_id
        self.course_id = course_id


# users class

class User(db.Model,UserMixin):
    """This class defines the schema for the users.
    It will responsible to allow the users to register based on roles"""

    # fields definition
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    hash_password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
            nullable=True)
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'),
            nullable=True)  

    # constructor
    def __init__(self, username, password, role, student_id, university_id):
        self.username = username
        self.hash_password = generate_password_hash(password, method='sha256')
        self.role = role
        self.student_id = student_id
        self.university_id = university_id
        

# registeration class

class Registered(db.Model):
    """This class defines the schema for the student registration."""

    # fields definition
    # id = db.Column(db.Integer, primary_key=True)
    registration_no = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
            nullable=False)
    academic_year = db.Column(db.String(64), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)  

    # constructor
    def __init__(self, registration_no, student_id, academic_year):
        self.registration_no = registration_no
        self.student_id = student_id
        self.academic_year = academic_year


# Tuition class

class Tuition(db.Model):
    """This class defines the schema for the course tuition."""

    # fields definition
    # id = db.Column(db.Integer, primary_key=True)
    receipt_no = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
            nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    academic_year = db.Column(db.String(64), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)  

    # constructor
    def __init__(self, receipt_no, student_id, amount_paid, balance, academic_year):
        self.receipt_no = receipt_no
        self.student_id = student_id
        self.amount_paid = amount_paid
        self.balance = balance
        self.academic_year = academic_year


# Application Fee class

class ApplicationFee(db.Model):
    """This class defines the schema for the course applcation fee."""

    # fields definition
    # id = db.Column(db.Integer, primary_key=True)
    receipt_no = db.Column(db.Integer, primary_key=True)
    application_no = db.Column(db.Integer, db.ForeignKey('application.id'),
            nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)  

    # constructor
    def __init__(self, receipt_no, application_no, amount_paid):
        self.receipt_no = receipt_no
        self.application_no = application_no
        self.amount_paid = amount_paid