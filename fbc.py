#!/usr/bin/python
# auth.py 
# Author: Muhammad M. Sesay

from . import db
from .models import User, Student, Faculty, Course, Module
from flask_login import login_user, logout_user, login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, make_response, session as login_session
from flask_cors import CORS
import string
import random
import json

# blueprint object
fbc = Blueprint('fbc', __name__)

CORS(fbc) # enable CORS on the auth blue print

# """ JOB SEEKER ROUTES BLOCK """

# generating a random string + digits as a token
token = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))

############################ SYSTEM ADMIN ROUTES #############################

# system admin dashboard route
@fbc.route('/system-admin/dashboard', methods=['GET'])
def systemAdminDashboard():
    # code goes here... maej
    return make_response(jsonify('system admin dashboard page'))

# all universities route
@fbc.route('/system-admin/universities')
def universities():
    # code goes here... maej
    return make_response(jsonify('all universites page'))

# new university route
@fbc.route('/system-admin/university/new')
def newUniversity():
    # code goes here... maej
    return make_response(jsonify('new university page'))

# single university route
@fbc.route('/system-admin/university/<university_name>', methods=['GET','POST'])
def singleUniversity(university_name):
    # code goes here... maej
    return make_response(jsonify('single university page'))

# edit university route
@fbc.route('/system-admin/university/<university_name>/edit', methods=['GET','POST'])
def editUniversity(university_name):
    # code goes here... maej
    return make_response(jsonify('edit university page'))

# delete university route
@fbc.route('/system-admin/university/<university_name>/delete', methods=['GET','POST'])
def deleteUniversity(university_name):
    # code goes here... maej
    return make_response(jsonify('delete univeresity page'))

############################ END OF SYSTEM ADMIN ROUTES ######################

############################ DEFAULT ROUTES ################################

# index route
@fbc.route('/usl/fbc')
def index():
    # code goes here... maej
    return make_response(jsonify('fbc index page'))

# about route
@fbc.route('/usl/fbc/about')
def about():
    # code goes here... maej
    return make_response(jsonify('fbc about page'))

# contact route
@fbc.route('/usl/fbc/contact')
def contact():
    # code goes here... maej
    return make_response(jsonify('fbc contact page'))

# login route
@fbc.route('/usl/fbc/student/login', methods=['GET','POST'])
@fbc.route('/usl/fbc/admin/login', methods=['GET','POST'])
def login():
    # code goes here... maej
    return make_response(jsonify('fbc admin and student login page'))
 
# logout route goes here
@fbc.route('/usl/fbc/logout', methods=['GET','POST'])
def logout():
    # code goes here... maej
    return make_response(jsonify('fbc logout page'))

############################ END OF DEFAULT ROUTES ###########################

# admin route
@fbc.route('/usl/fbc/admin/dashboard')
def adminDashboard():
    # code goes here... maej
    return make_response(jsonify('fbc admin dashboard page'))


############################ FACULTY ROUTES #################################

# all faculty route
@fbc.route('/usl/fbc/faculty')
def faculty():
    # code goes here... maej
    return make_response(jsonify('fbc faculty page'))

# specific faculty route
@fbc.route('/usl/fbc/faculty/<faculty_name>')
def singleFaculty(faculty_name):
    # code goes here... maej
    return make_response(jsonify('fbc single faculty page'))

# new faculty route
@fbc.route('/usl/fbc/faculty/new')
def newFaculty():
    # code goes here... maej
    return make_response(jsonify('fbc new faculty page'))

# edit faculty route
@fbc.route('/usl/fbc/faculty/<faculty_name>/edit', methods=['GET','POST'])
def editFaculty(faculty_name):
    # code goes here... maej
    return make_response(jsonify('fbc edit faculty page'))

# delete faculty route
@fbc.route('/usl/fbc/faculty/<faculty_name>/delete', methods=['GET','POST'])
def deleteFaculty(faculty_name):
    # code goes here... maej
    return make_response(jsonify('fbc delete faculty page'))

############################ END OF FACULTY ROUTES ###########################

############################ COURSE ROUTES #################################

# all course route
@fbc.route('/usl/fbc/courses')
def courses():
    # code goes here... maej
    return make_response(jsonify('fbc courses page'))

# specific course route
@fbc.route('/usl/fbc/courses/<course_name>')
def singleCourse(course_name):
    # code goes here... maej
    return make_response(jsonify('fbc single course page'))

# new course route
@fbc.route('/usl/fbc/courses/new')
def newCourse():
    # code goes here... maej
    return make_response(jsonify('fbc new course page'))

# edit course route
@fbc.route('/usl/fbc/courses/<course_name>/edit', methods=['GET','POST'])
def editCourse(course_name):
    # code goes here... maej
    return make_response(jsonify('fbc edit course page'))

# delete course route
@fbc.route('/usl/fbc/courses/<course_name>/delete', methods=['GET','POST'])
def deleteCourse(course_name):
    # code goes here... maej
    return make_response(jsonify('fbc delete course page'))

############################ END OF COURSE ROUTES ###########################

############################ MODULE ROUTES #################################

# all module route
@fbc.route('/usl/fbc/modules')
def modules():
    # code goes here... maej
    return make_response(jsonify('fbc modules page'))

# specific module route
@fbc.route('/usl/fbc/modules/<module_name>')
def singleModule(module_name):
    # code goes here... maej
    return make_response(jsonify('fbc single module page'))

# new module route
@fbc.route('/usl/fbc/modules/new')
def newModule():
    # code goes here... maej
    return make_response(jsonify('fbc new module page'))

# edit module route
@fbc.route('/usl/fbc/modules/<module_name>/edit', methods=['GET','POST'])
def editModule(module_name):
    # code goes here... maej
    return make_response(jsonify('fbc edit module page'))

# delete module route
@fbc.route('/usl/fbc/modules/<module_name>/delete', methods=['GET','POST'])
def deleteModule(module_name):
    # code goes here... maej
    return make_response(jsonify('fbc delete module page'))

############################ END OF MODULE ROUTES ###########################

################## APPLICATION & REGISTRATION ROUTES ########################

# all applicants route
@fbc.route('/usl/fbc/courses/applicants')
def applicants():
    # code goes here... maej
    return make_response(jsonify('fbc all applicants page'))

# specific applicant's route
@fbc.route('/usl/fbc/courses/applicants/<applicant_name>')
def singleApplicant(applicant_name):
    # code goes here... maej
    return make_response(jsonify('fbc single applicant page'))

# registeration route
@fbc.route('/usl/fbc/courses/registered')
def registered():
    # code goes here... maej
    return make_response(jsonify('fbc all registered student page'))

# specific registered student route
@fbc.route('/usl/fbc/courses/registered/<student_name>', methods=['GET','POST'])
def singleRegisteredStudent(student_name):
    # code goes here... maej
    return make_response(jsonify('fbc single registered student page'))

################## END OF APPLICATION & REGISTRATON ROUTES #######################

################################ FEES ROUTES #####################################

# course applicaation fee route
@fbc.route('/usl/fbc/courses/<course_name>/application-fee', methods=['GET','POST'])
def courseApplicationFee(course_name):
    # code goes here... maej
    return make_response(jsonify('fbc course applicaton fee page'))

# course tuition fee route
@fbc.route('/usl/fbc/courses/<course_name>/tuition-fee', methods=['GET','POST'])
def courseTuitionFee(course_name):
    # code goes here... maej
    return make_response(jsonify('fbc course tuition fee page'))

################################ END OF FEES ROUTES ###############################

################################ STUDENT ROUTES #####################################

# student freshmen application route
@fbc.route('/usl/fbc/freshmen/enrollment', methods=['GET','POST'])
def freshmen():
    # code goes here... maej
    return make_response(jsonify('fbc freshmen application route'))

# student dashboard route
@fbc.route('/usl/fbc/student/dashboard', methods=['GET','POST'])
def studentDashboard():
    # code goes here... maej
    return make_response(jsonify('fbc student dashboard'))

# student profile route
@fbc.route('/usl/fbc/student/profile', methods=['GET','POST'])
def studentProfile():
    # code goes here... maej
    return make_response(jsonify('fbc student profile'))

# student registration route
@fbc.route('/usl/fbc/student/registration', methods=['GET','POST'])
def studentRegistration():
    # code goes here... maej
    return make_response(jsonify('fbc student registration page'))

# student payment route
@fbc.route('/usl/fbc/student/pay-tuition', methods=['GET','POST'])
def studentPayment():
    # code goes here... maej
    return make_response(jsonify('fbc student payment page'))

################################ END OF STUDENT ROUTES ###############################

# jobseeker login auth route
# @fbc.route('/api/v1/portal/jsk/login', methods=['GET', 'POST'])
# def jskLogin():
#     """This function runs authentication checks on the user."""

#     # saving the session in a token
#     login_session['token'] = token

#     if request.method == 'POST':

#         data = request.get_json()

#         email = data['email']
#         password = data['password']
#         client_token = data['token']

#         # check if the token matches
#         if client_token != login_session['token']:
#             return make_response(jsonify({'error':'Invalid token'}), 401) # response
#         else: 
#             # fetch the user
#             user = User.query.filter_by(email=email).first()

#             # validate user and password
#             if not user or not user.check_password(password):
#                 return make_response(
#                     jsonify({'error':'Invalid username or password.'}), 
#                     500) # if user doesn't exist or password is wrong, reload the page

#             login_user(user)

#             # return redirect(url_for('auth.jskDashboard'))

#             return redirect(url_for('auth.jskDashboard', userId=current_user.id))

#             # login_session['userId'] = current_user.id

#             # return make_response(jsonify({'success':current_user.id}), 200)

#     return make_response(jsonify({'token': token}), 200)  # response

# jobseeker signup auth route
# @auth.route('/api/v1/portal/jsk/signup', methods=['GET', 'POST'])
# def jskSignup():
#     """This function allows the creation of a jobseeker account."""

#     if request.method == 'POST':

#         # get the json data
#         data = request.get_json()

#         first_name = data['first_name']
#         last_name = data['last_name']
#         email = data['email']
#         password = data['password']
#         confirm_password = data['confirm_password']

#         # output = "{} -->{} -->{} -->{} -->{}".format(first_name,
#         #                                         last_name,
#         #                                         email,
#         #                                         password,
#         #                                         confirm_password)

#         # return output

#         # if this returns a user, then the email already exists in database
#         user = Jobseeker.query.filter_by(email=email).first()

#         # if a user is found, we want to redirect back to signup page so user can try again
#         if user:
#             return make_response(jsonify({'error':'A user with that email already exists'}), 500)

#         # check if passwords match
#         elif password != confirm_password:
#             return make_response(jsonify({'error':'Password donot match.'}), 500)

#         # if password is greater than 6 digits
#         # elif len(password) < 6:
#         #     return make_response(jsonify({'error':'Passwords must greater than six characters.'}), 500)

#         # create new user with the form data. Hash the password so plaintext version isn't saved.
#         new_user = Jobseeker(first_name=first_name, last_name=last_name, 
#                             email=email, password=password)

#         # add the new user to the database
#         db.session.add(new_user)
#         db.session.commit()
#         return make_response(jsonify({'success':'new jobseeker account created'}), 201)
            
#     return "welcome"#  render_template('signup.html')

# # jobseeker list of jobs route
# @auth.route('/api/v1/portal/jsk/all-jobs')
# def jskJobs():
#     """This function returns all the jobs a jobseeker have applied for."""
#     return 'here are the jobs...'

# # jobseeker dashboard route
# @auth.route('/api/v1/portal/jsk/dashboard/<int:userId>', methods=['GET','POST'])
# def jskDashboard(userId):
#     """This function returns the jobseekers dashboard."""

#     userId = 3

#     # fetch the user
#     user = Jobseeker.query.filter_by(id=userId).first()

#     # if user:
#     return make_response(jsonify({'userDetail': user.serialize}), 200)

#     # return make_response(jsonify({'res': userId}), 200)
    

#         # userId = current_user.id
#         # userOne = login_session['userDetail']
#         # userId = userOne
#         # user = Jobseeker.query.filter_by(id=userId).first()

#         # print(login_session['userDetail'])
#     #user = Jobseeker.query.all()
#         # objUser=[user.serialize] result.serialize()
#         # json_data = json.dumps(user, indent=2)
#         # print(json_data)
#         # print(json.loads(json_data))
#         # return make_response(jsonify({'userDetails':user}), 200)
    
#     # redirect the user to the user to the login page if logging session if false
#     # return make_response(jsonify({'error':'please login to access the resource'}), 500)
#     # return make_response(jsonify('request reached'))

# # logout route
# @auth.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('main.index'))


# # """ ORGANIZATION ROUTES BLOCK """

# # @auth.route('/portal/org/dashboard')
# # def orgHome():
# #     """This function display the organizations resources."""
# #     return 'welcome organization'

# # organization login auth route
# @auth.route('/api/v1/portal/org/login', methods=['GET', 'POST'])
# def orgLogin():
#     """This function runs authentication checks on the organization."""

#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')

#         organ = Organization.query.filter_by(email=email).first()

#         # check if user actually exists
#         # take the user supplied password, hash it, and compare it to the hashed password in database
#         if not organ or not organ.check_password(password): 
#             flash('Please check your login details and try again.')
#             return redirect(url_for('auth.orgLogin')) # if user doesn't exist or password is wrong, reload the page

#         login_user(organ)  # login the user

#         # saving the requested page as next
#         next = request.args.get('next')

#         # if the request is none
#         if next is None or not next[0] == '/portal/org/dashboard':
#             next = url_for('main.orgDashboard')
#         # redirecting to the prevoius or next url
#         return redirect(next)

#         # # if the above check passes, then we know the user has the right credentials
#         # return redirect(url_for('main.profile'))

#     return render_template('login_org.html')

# # organization signup auth route
# @auth.route('/api/v1/portal/org/signup', methods=['GET', 'POST'])
# def orgSignup():
#     """This function executes the creation of an organization account."""

#     if request.method == 'POST':
#         # get the data from the request and store them in the 
#         # data variable
#         data = request.get_json()

#         first_name = data['first_name'] 
#         last_name = data['last_name'] 
#         jobtitle = data['jobtitle'] 
#         phone = data['phone'] 
#         company_name = data['company_name']
#         email = data['email'] 
#         address = data['address'] 
#         city = data['city'] 
#         district = data['district'] 
#         industry = data['industry'] 
#         bio = data['bio'] 
#         password = data['password']
#         confirm_password = data['confirm_password']

#         # if this returns a user, then the email already exists in database
#         organizationAdmin = Organization.query.filter_by(email=email).first()

#         # if a user is found, we want to redirect back to signup page so user can try again
#         # if organizationAdmin:
#         #     flash('A organization with that email already exist.')
#         #     return redirect(url_for('auth.orgSignup'))

#         # # check if passwords match
#         # elif password != confirm_password:
#         #     flash('Password donot match.')
#         #     return redirect(url_for('auth.orgSignup'))

#         # if password is greater than 6 digits
#         # if password < 6:
#         # create new user with the form data.
#         new_orgnisation = Organization(first_name=first_name, last_name=last_name,
#             jobtitle=jobtitle, phone=phone, company_name=company_name, email=email,
#             address=address, city=city, district=district, industry=industry,
#             bio=bio, password=password)

#         # add the new user to the database
#         db.session.add(new_orgnisation)
#         db.session.commit()

#         return make_response(jsonify('the data saved successfully'), 200)
#         # return redirect(url_for('auth.orgLogin'))
#         # flash('Password should be greater than 6.')
            
#     # return make_response(jsonify(data), 200)

# # # organization all posted jobs route

# @auth.route('/api/v1/portal/org/jobs')
# def orgAllJobs():
#     """This function returns all jobs posted by a organizations
#     displaying in an DESC format."""
#     return 'showing all org jobs...'

# # organization all job applicants route


# @auth.route('/api/v1/portal/org/jobs/<jobTitle>/applicants')
# def orgAllJobApplicants(jobTitle):
#     """This function returns all the applicants of a specific job."""
#     return 'showing all {} job applicants'.format(jobTitle)

# # organization specific job applicants route


# @auth.route('/api/v1/portal/org/jobs/<jobTitle>/applicants/<applicantName>')
# def orgSpecificJobApplicant(jobTitle, applicantName):
#     """This function returns a specifc applicant details."""
#     return 'showing applicant {} from {} job'.format(applicantName, jobTitle)

# # organization create job route


# @auth.route('/api/v1/portal/org/job/new')
# def orgCreateJob():
#     """This function enables the creation of a new job."""
#     return 'creating a new job...'

# # organization edit job route


# @auth.route('/api/v1/portal/org/jobs/<jobTitle>/edit')
# def orgEditJob(jobTitle):
#     """This function enables the editing of a job."""
#     return 'editing job {}...'.format(jobTitle)

# # organization delete job route


# @auth.route('/api/v1/portal/org/jobs/<jobTitle>/delete')
# def orgDeleteJob(jobTitle):
#     """This function enables the deleting of a ob."""
#     return 'deleting job {}...'.format(jobTitle)