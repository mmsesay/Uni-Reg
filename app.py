#!/usr/bin/python
import os
import csv
from datetime import datetime
from flask import Flask, render_template, request, redirect,jsonify, url_for
from flask import flash, make_response, abort, session as login_session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './documents/files'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# login manager object
login_manager = LoginManager()

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from database_setup import Base, User, Contract

# imports for random string generation
import random
import string
 
# importing the oauth modules
import json

# app secret
app.config['SECRET_KEY'] = 'mysecretkey'

#Connect to Database and create database session
engine = create_engine('sqlite:///sl_uni.db?check_same_thread=False')

# setting the app to make use of login manager
login_manager.init_app(app)
login_manager.login_view = 'login'

# bind the engine
Base.metadata.bind = engine

# binding the engine
DBSession = sessionmaker(bind=engine)
session = DBSession()  # session object

# getting the current date and time
now = datetime.now() 

# login manager function
@login_manager.user_loader
def load_user(user_id):
    """This function loads the user."""
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        flash('invalid username or password')
        abort(400)
    return user

# verfiy the uploaded file formats
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

###################### LOG ENTRIES #########################
# user account creation log function
def newUserLog(createdUser,creator):
    """This fucntion creates a log for the newly registered user"""

    with open('./csv_files/newUser.csv', mode='a', newline='') as csvfile:

        # fieldnames decalaration
        fieldnames = ['Created_username', 'Creator', 'Date', 'Time']
        
        # define the writer object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        try:
            createdUser = createdUser.capitalize()
            creator = creator.capitalize()
            date = now.strftime("%m/%d/%Y")[:11]
            time = now.strftime("%H:%M:%S")[:9]
            
        except ValueError:
            return make_response(jsonify({'error':'unable to process data'}), 500)
        finally:
            writer.writerow({'Created_username':createdUser, 'Creator':creator, 'Date':date, 'Time':time})
            return make_response(jsonify({'success':'data processed successfully'}), 200)

# user login log function
def userLoginLog(username):
    """This fucntion creates a log for the newly registered user"""

    with open('./csv_files/login.csv', mode='a', newline='') as csvfile:

        # fieldnames decalaration
        fieldnames = ['Username', 'Date', 'Time']
        
        # define the writer object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        try:
            username = username.capitalize()
            date = now.strftime("%m/%d/%Y")[:11]
            time = now.strftime("%H:%M:%S")[:9]
            
        except ValueError:
            return make_response(jsonify({'error':'unable to data'}), 500)
        finally:
            writer.writerow({'Username':username, 'Date':date, 'Time':time})
            return make_response(jsonify({'success':'data processed successfully'}), 200)

# user login log function
def contractCreationLog(creator, contractorName):
    """This fucntion creates a log for the newly registered user"""

    with open('./csv_files/contractCreationLog.csv', mode='a', newline='') as csvfile:

        # fieldnames decalaration
        fieldnames = ['Creator', 'ContractorName', 'Date', 'Time']
        
        # define the writer object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        try:
            creator = creator.capitalize()
            contractorName = contractorName.capitalize()
            date = now.strftime("%m/%d/%Y")[:11]
            time = now.strftime("%H:%M:%S")[:9]
            
        except ValueError:
            return make_response(jsonify({'error':'unable to data'}), 500)
        finally:
            writer.writerow({'Creator':creator, 'ContractorName':contractorName, 'Date':date, 'Time':time})
            return make_response(jsonify({'success':'data processed successfully'}), 200)

###################### END OF LOG ENTRIES ##################

# user login route
@app.route('/', methods = ['GET','POST'])
def login():  
    """This function returns the login template and perform the relevant checks
    to authenticate a user."""

    # generating a random string + digits as a state
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    # saving that state to an array object
    login_session['state'] = state

    # check if the request made is a post
    if request.method == 'POST':
        
        username = request.form['username'].capitalize()
        password = request.form['password']

        # is username and password are inputed
        if username and password is not '':

            # retrieve the username and store in an object
            user = session.query(User).filter_by(username=username).first()

            # verifying the user password and the user object
            if user.verify_password(password) and user is not '':

                login_session['logged in'] = True # setting the user logged in session
                login_user(user) # login the user
                userLoginLog(username)  # pass the login username to save in the log file

                # saving the requested page as next
                next = request.args.get('next')

                # if the request is none
                if next == None or not next[0] == '/admin/dashboard':
                    next = url_for('dashboard')
                return redirect(next) # redirecting to the prevoius or next url
            else:
                # throw error if no match for username or password
                flash("invalid username or password")
        else:
            # throw this error message if the username and password fields are
            # empty
            flash("username and password are required")

    # return if the request is GET and passing the current session state from
    # login_session['state'] object
    return render_template('login.html', STATE=state)

# user logout route
@app.route('/logout')
@login_required
def logout():
    """This function logout's a user"""
    logout_user()
    flash("you are logged out")
    return redirect(url_for('login'))

# all admin user api endpoint
# @app.route('/orange/contract/admin/api/v1/JSON')
# def adminJSON():
#     """This api function return all the administartors from the db."""
#     allAdmin = session.query(Admin).all()
#     return jsonify(Admins=[cat.serialize for cat in allAdmin])
    
# dashboard route
@app.route('/app/orange-contract-system/dashboard', methods = ['GET'])
@login_required
def dashboard():

    if current_user.is_authenticated:
        allContracts = session.query(Contract).all()

        # fetch the match id of the current logged in user
        userDetials = session.query(User).filter_by(id=current_user.id).first()

        # check if this is first time user login
        if userDetials.initial_login == 0:
            flash('Hello {}, please change your password'.format(userDetials.username))

            return redirect(url_for('user_account'))

        return render_template('dashboard.html', contracts=allContracts,
                                nav='home')

    flash('Please login to gain access') # flashing a successful message
    return redirect(url_for('login')) # redirecting the user

# new user creation route
@app.route('/app/orange-contract-system/register/new/user', methods = ['GET','POST'])
@login_required
def register():
    """This function handles the registration of a new user."""

    # checking if the request was a post
    if request.method == 'POST':

        # fetching the data from the form and storing in variables
        username = request.form['username'].capitalize()
        email = request.form['email']
        account_type = request.form['account_type']
        password = request.form['password']

        # is username and password are not empty
        if username and email and account_type and password != '':
            
            # check if an email is not match was False
            if session.query(User).filter_by(email=email).first() is None:

                # check for whitespace in username field
                if ' ' in username:
                    flash('Username must be one word. No whitespace is allowed!')

                else:
                    # check the password length
                    if len(password) > 6:

                        # retrieve the username and store in an object
                        user = session.query(User).filter_by(id=current_user.id).first()
                        creator = user.username

                        # storing the User data to an object 
                        newUser = User(username=username, email=email, account_type=account_type,
                                    initial_login=0, password=password)
                        session.add(newUser) # adding the object
                        session.commit() # saving the object to the database
                        newUserLog(username,creator)  # creating the log file
                        flash('Thanks for signing up. Please login') # flashing a successful message
                        return redirect(url_for('login')) # redirecting the user

                    else:
                        # throw error message if a password length is less than 6
                        flash('Your password must be at least 6 characters')
            else:
                # throw error message if an email already exist
                flash('username is already existing')
        else:
            # throw this error message if the input fields are empty
            flash('All fields are required')

    # render if the request was a GET
    return render_template('dashboard.html', nav='register')


# all contracts view
@app.route('/app/orange-contract-system/contracts', methods = ['GET', 'POST'])
@login_required
def allContracts():
    """This function returns all the contracts"""

    # popUp = 'false'

    if request.method == 'GET':
        allContracts = session.query(Contract).all()

        return render_template('dashboard.html', contracts=allContracts,
        nav='all_contracts', active='True')


# notifications route
@app.route('/app/orange-contract-system/notifications', methods = ['GET', 'POST'])
def notifications():

    # check the request type
    if request.method == 'POST':
        return 'all notifications'

    # if the request was a get
    return 'showning all notifications'


# create a new contract api
@app.route('/app/orange-contract-system/create-contract', methods=['GET','POST'])
@login_required
def createContract():
    """ This function return the view for the creation of a new contract."""

    if request.method == 'POST':

        # fetching the data from the form and storing in variables
        companyName = request.form['company_name']
        company_address = request.form['company_address']
        company_mobile = request.form['company_mobile']
        contract_type = request.form['contract_type']
        signed_date = request.form['signed_date']
        expiration_date = request.form['expiration_date']
        file = request.files['file']

        # check if the post request has the file part
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        # file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)

        # check if the fields are not empty
        if companyName and company_address and company_mobile and contract_type and signed_date and expiration_date != '':

            # check if a contract name is not match was False
            if session.query(Contract).filter_by(company_name=companyName).first() is None:
                # save the current logged in user id
                userId = current_user.id

                filename = ''  # setting the filename empty by default

                # check if no file was chosen
                if file.filename == '':
                    filename = ''

                    # storing the new data to an object 
                    newContract = Contract(company_name=companyName, company_address=company_address,
                        company_mobile=company_mobile, contract_document=filename, contract_type=contract_type,
                        signed_date=signed_date, expiration_date=expiration_date,user_id=userId)

                    session.add(newContract) # adding the object
                    session.commit() # saving the object to the database
                    flash('New contract between {} created'.format(companyName))

                    # store the current username 
                    creator = current_user.username
                    contractCreationLog(creator, companyName)  # pass them to the log
                
                # check if the file is allowed for processing
                elif file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                    # storing the new data to an object 
                    newContract = Contract(company_name=companyName, company_address=company_address,
                        company_mobile=company_mobile, contract_document=filename, contract_type=contract_type,
                        signed_date=signed_date, expiration_date=expiration_date,user_id=userId)

                    session.add(newContract) # adding the object
                    session.commit() # saving the object to the database
                    flash('New contract between {} created'.format(companyName))

                    # store the current username 
                    creator = current_user.username
                    contractCreationLog(creator, companyName)  # pass them to the log
                
                else:
                    flash('Error: documents should be in (pdf, png, jpg, jpeg) formats')
            else:
                # throw error message if a company with the passed name is already existing
                flash('company name {} is already existing'.format(companyName))
        else:  
            # throw this error message if the input fields are empty
            flash('Please fill in all input required')
    
    # return view if the request is a get
    return render_template('dashboard.html', nav='contract')

# edit contract function
@app.route('/app/orange-contract-system/<companyName>/edit', methods=['GET', 'POST'])
@login_required
def editContract(companyName):
    """This function allows ordaniary users to edit contracts
    and send the request to the admin for approval."""

    # approval state
    approved = False

    # fetching a single category from the db and storing it in an object
    fetchCompany = session.query(
        Contract).filter_by(company_name=companyName).first()

    # if the request is a POST
    if request.method == 'POST':
        try:

            companyName = request.form['company_name']
            company_address = request.form['company_address']
            company_mobile = request.form['company_mobile']
            contract_type = request.form['contract_type']
            signed_date = request.form['signed_date']
            expiration_date = request.form['expiration_date']

            # fetchCompany.company_name = request.form['company_name']
            # fetchCompany.company_address = request.form['company_address']
            # fetchCompany.company_mobile = request.form['company_mobile']
            # fetchCompany.contract_type = request.form['contract_type']
            # fetchCompany.signed_date = request.form['signed_date']
            # fetchCompany.expiration_date = request.form['expiration_date']

            # check if the company name field is empty
            if companyName == '':
                # set data as it is
                fetchCompany.company_name = fetchCompany.company_name
            else:
                # modify the existing data
                fetchCompany.company_name = companyName
            
            # check company address
            if company_address == '':
                # set data as it is
                fetchCompany.company_address = fetchCompany.company_address
            else:
                # modify the existing data
                fetchCompany.company_address = company_address
            
            # check company mobile
            if company_mobile == '':
                # set data as it is
                fetchCompany.company_mobile = fetchCompany.company_mobile
            else:
                # modify the existing data
                fetchCompany.company_mobile = company_mobile
            
            # check contract_type
            if contract_type == '':
                # set data as it is
                fetchCompany.contract_type = fetchCompany.contract_type
            else:
                # modify the existing data
                fetchCompany.contract_type = contract_type
            
            # check signed_date
            if signed_date == '':
                # set data as it is
                fetchCompany.signed_date = fetchCompany.signed_date
            else:
                # modify the existing data
                fetchCompany.signed_date = signed_date

            # check expiration date
            if expiration_date == '':
                # set data as it is
                fetchCompany.expiration_date = fetchCompany.expiration_date
            else:
                # modify the existing data
                fetchCompany.expiration_date = expiration_date
            
            # check the users account type
            if current_user.account_type == 'ordinary':
                flash('Edit request has been sent to system\'s administrator')

        except:
            pass
        # else:  
        #     # throw this error message if the input fields are empty
        #     flash('Please fill in all input required')
#         session.add(fetchCompany)  # saving the new category name
#         session.commit()
#         # flashing a successful message
#         flash(
#             'Company \'{}\' updated to successfully'.format(categoryName))

    #         # check if the form was not empty
    #         if request.form['name'] is not '':

    #             # fetching a single category from the db and store in object
    #             fetchOneCompany = session.query(
    #                 Contract).filter_by(company_name=cName).one()

    #             if fetchedCategory.name != request.form['name']:
    #                 # to fix 
    #                 category = session.query(Category).filter_by(
    #                     id=fetchedCategory.id).one()

    #                 # check if object name didn't match the form input name
    #                 if category.name != request.form['name']:

    #                     try:

    #                         # assign the new name to fetchedCategory
    #                         category.name = request.form['name']
    #                         session.add(category)  # saving the new category name
    #                         session.commit()
    #                         # flashing a successful message
    #                         flash(
    #                             'Category \'{}\' updated to \'{}\''.format(
    #                                 categoryName, request.form['name']))
    #                         # redirecting the user
    #                         return redirect(
    #                             url_for(
    #                                 'allCategories',
    #                                 user_id=category.user_id))
    #                     except:
    #                         session.rollback()
    #                         raise
    #             else:
    #                 flash(
    #                     'Sorry \'{}\' category is already existing.'
    #                     'Input another name'.format(request.form['name']))
    #         else:
    #             flash('a category name is required')

    #     flash("""Edit Operation failed! Your are not the creator of \'{}\'
    #     category""".format(categoryName))
    return render_template('dashboard.html', company=fetchCompany, nav='edit_contract')

# user accout function
@app.route('/app/orange-contract-system/my-account', methods=['GET','POST'])
@login_required 
def user_account():

    # retrieve the user 
    userData = session.query(User).filter_by(id=current_user.id).first()

    # check for post request
    if request.method == 'POST':
        
        # store the inputs requests
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # is username and password are inputed
        if password or confirm_password != '':
            
            # verify if the passwords match
            if password == confirm_password:

                # retrieve the user 
                user = session.query(User).filter_by(id=userData.id).first()

                # check the lenght of the password
                if len(password) > 6:
                    
                    # assign the new updates
                    user.hash_password = generate_password_hash(password)
                    user.initial_login = 1  # update the initial_login
                    session.add(userData)  # adding the update
                    session.commit()  # saving the data
                    # flashing a successful message
                    flash('your password was successfully changed')
                    # redirecting the user
                    return redirect(url_for('user_account'))

                else:
                    flash('your password must be more than 6 characters')
            else:
                # otherwise return error message
                flash('passwords donot match')
            # retrieve the username and store in an object
            # user = session.query(User).filter_by(username=username).first()

            # # verifying the user password and the user object
            # if user.verify_password(password) and user is not '':
            #     pass
        else:
            # return error message if the fields are empty
            flash('please fill in the input fields')

    return render_template('dashboard.html', user=userData, nav='user_account')

# main function
if __name__ == "__main__":
    app.debug = True
    app.run(host='127.0.0.1', port=7000)
