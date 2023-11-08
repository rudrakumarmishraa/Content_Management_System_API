# Importing packages to be used....
from flask import Flask, request
from flask_cors import cross_origin
import pymongo
import uuid
import json



# Initialised App object and other variables essential for app....
app = Flask(__name__)
SECRET_KEY = 'SECRET_KEY '
app.config['CORS_HEADERS'] = 'Content-Type'
# Database client and db database object intialized....
DATABASE_URI = 'DATABASE_URI'
dbClient = pymongo.MongoClient(DATABASE_URI)
db = dbClient['DATABASE']


#####################################################################################################################
################################################ CMS USER OPERATIONS ################################################
#####################################################################################################################


# Main route of app Home Page of API....
@app.route('/', methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
@cross_origin()
def index():
    if(request.method == 'GET'):
        return {"Content Management System API": "Content Management System API is used to create frontend CMS application on any framework such as React.js and Next.js. It currently provides operations such as User CRUD for CMS Web Appication and API CRUD for users, which will be further scaled to provide analytics on data provided by users.",
    "Imported packages to be used": "We are using Flask package to intialise our app and to create and run server and requests to get HTTP request and its parameter for doing backend operations and sending response. We are using pymongo to access our backend MongoDB database and perform different CRUD operations which is hosted on Clever-Cloud platform. We are using UUID package to generate random ID's which are used as API_KEY for users for Content Management System. We are using json package to convert Strings into json data or python Dict."}
    else:
        return {'Method Error': 'Only GET method allowed on this endpoint.', 'request-type': request.method}


# API endpoint for creating User saving it to backend Mongoose Database and Returning Reposnse Object for CMS platform....
@app.route('/api/v1/create_user', methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
@cross_origin()
def create_user():
    # Table where data is stored....
    collection = db[SECRET_KEY]
    # If Request Method is POST....
    if(request.method=='POST'):
        # If correct SECRET_KEY passed to the API endpoint....
        if(request.args.get('SECRET_KEY') == SECRET_KEY):
            # Getting request parameters....
            id = str(uuid.uuid1())
            username = request.args.get('username')
            password = request.args.get('password')
            email = request.args.get('email')
            API_KEY = str(uuid.uuid1())
            # If username or email or password parameter not provided....
            if((username is None) or (email is None)  or (password is None)):
                # Returning error message....
                return {'Error': {'Parameters not specified correctly.' : 'You need to provide email, password and name.', 'user': {'id': id, 'firstName': str(request.args.get('firstName')), 'lastName': str(request.args.get('lastName')), 'username': str(username), 'password': str(password), 'email': str(email), 'mobileNumber': str(request.args.get('mobileNumber')), 'address': str(request.args.get('address'))}}}
            else:
                # If username or email or password parameter blank....
                if(username == '' or password == '' or email == ''):
                    # Returning error message....
                    return {'Error': {'Parameter specified but not set' : "Email, password and name parameters cann't be empty.", 'user': {'id': id, 'firstName': str(request.args.get('firstName')), 'lastName': str(request.args.get('lastName')), 'username': str(username), 'password': str(password), 'email': str(email), 'mobileNumber': str(request.args.get('mobileNumber')), 'address': str(request.args.get('address'))}}}
                else:
                    # Write code for pushing the User to backend Database....
                    # Checking if username already exists....
                    if(collection.find_one({'username': username})):
                        return {'Error': {'Duplicate Username' : "Username already exists."}}
                    # Checking if email already exists....
                    elif(collection.find_one({'email': email})):
                        return {'Error': {'Duplicate Email' : "Email already exists."}}
                    else:
                        # If unique record then push to database.... 
                        collection.insert_one({'id': id, 'firstName': str(request.args.get('firstName')), 'lastName': str(request.args.get('lastName')), 'username': str(username), 'password': str(password), 'email': str(email), 'mobileNumber': str(request.args.get('mobileNumber')), 'address': str(request.args.get('address'))})
                        # Message for the User Because User Created....
                        return {'Success': 'Successfully Created a User', 'Created': {'id': id, 'firstName': str(request.args.get('firstName')), 'lastName': str(request.args.get('lastName')), 'username': str(username), 'password': str(password), 'email': str(email), 'mobileNumber': str(request.args.get('mobileNumber')), 'address': str(request.args.get('address'))}}
        else:
            return {'Authentication Error': 'SECRET_KEY Provided is Wrong.', 'SECRET_KEY': request.args.get('SECRET_KEY')}
    else:
        return {'Method Error': 'Only post method allowed on this endpoint.', 'request-type': request.method}


# API endpoint to search user from database from backend Mongoose Database and Returning Reposnse Object for CMS platform....
@app.route('/api/v1/get_user', methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
@cross_origin()
def get_user():
    # Table where data is stored....
    collection = db[SECRET_KEY]
    # If Request Method is POST....
    if(request.method=='POST'):
        # If correct SECRET_KEY passed to the API endpoint....
        print(request.args)
        if(request.args.get('SECRET_KEY') == SECRET_KEY):
            # Getting id of user to be searched....
            id = request.args.get('id')
            email = request.args.get('email')
            username = request.args.get('username')
            # If id is provided....
            if(id is not None and id != ''):
                # Getting data from id....
                data = collection.find_one({'id': id})
                # If user present....
                if(data):
                    return {'Success': 'Found the User.','user': {'id': data['id'], 'firstName': data['firstName'], 'lastName': data['lastName'], 'username': data['username'], 'email': data['email'], 'password': data['password'], 'address': data['address'], 'mobileNumber': data['mobileNumber']}}
                # If no user present with given id....
                else:
                    return {'Error': 'No such User exists.', 'id': id}
            # If email is provided....
            elif(email is not None and email != ''):
                # Getting data from email....
                data = collection.find_one({'email': email})
                # If user present....
                if(data):
                    return {'Success': 'Found the User.','user': {'id': data['id'], 'firstName': data['firstName'], 'lastName': data['lastName'], 'username': data['username'], 'email': data['email'], 'password': data['password'], 'address': data['address'], 'mobileNumber': data['mobileNumber']}}
                # If no user present with given email....
                else:
                    return {'Error': 'No such User exists.', 'email': email}
            # If username is provided....
            elif(username is not None and username != ''):
                # Getting data from username....                
                data = collection.find_one({'username': username})
                # If user present....
                if(data):
                    return {'Success': 'Found the User.','user': {'id': data['id'], 'firstName': data['firstName'], 'lastName': data['lastName'], 'username': data['username'], 'email': data['email'], 'password': data['password'], 'address': data['address'], 'mobileNumber': data['mobileNumber']}}
                # If no user present with given username....
                else:
                    return {'Error': 'No such User exists.', 'username': username}
            # If Parameters not specified correctly....
            else:
                return {'Error': {'Parameters not specified correctly.' : 'You need to provide id, email or username.'}}
        # Authentication Error API_KEY Provided is Wrong....
        else:
            return {'Authentication Error': 'SECRET_KEY Provided is Wrong.', 'SECRE_KEY': request.args.get('SECRET_KEY')}
    # Method Error Only post method allowed on this endpoint....
    else:
        return {'Method Error': 'Only post method allowed on this endpoint.', 'request-type': request.method}


# API endpoint to delete user from database from backend Mongoose Database and Returning Reposnse Object for CMS platform....
@app.route('/api/v1/delete_user', methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
@cross_origin()
def delete_user():
    # Table where data is stored....
    collection = db[SECRET_KEY]
    # If Request Method is POST....
    if(request.method=='POST'):
        # If correct SECRET_KEY passed to the API endpoint....
        if(request.args.get('SECRET_KEY') == SECRET_KEY):
            # Getting id of user to be searched....
            id = request.args.get('id')
            email = request.args.get('email')
            username = request.args.get('username')
            # If id is provided....
            if(id is not None and id != ''):
                # Getting data from id....
                data = collection.find_one({'id': id})
                # If user present....
                if(data):
                    collection.delete_one({'id': id})
                    return {'Success': 'Found and deleted User successfully.','user': {'id': data['id'], 'firstName': data['firstName'], 'lastName': data['lastName'], 'username': data['username'], 'email': data['email'], 'password': data['password'], 'address': data['address'], 'mobileNumber': data['mobileNumber']}}
                # If no user present with given id....
                else:
                    return {'Error': 'No such User exists.', 'id': id}
            # If email is provided....
            elif(email is not None and email != ''):
                # Getting data from email....
                data = collection.find_one({'email': email})
                # If user present....
                if(data):
                    collection.delete_one({'email': email})
                    return {'Success': 'Found and deleted User successfully.','user': {'id': data['id'], 'firstName': data['firstName'], 'lastName': data['lastName'], 'username': data['username'], 'email': data['email'], 'password': data['password'], 'address': data['address'], 'mobileNumber': data['mobileNumber']}}
                # If no user present with given email....
                else:
                    return {'Error': 'No such User exists.', 'email': email}
            # If username is provided....
            elif(username is not None and username != ''):
                # Getting data from username....                
                data = collection.find_one({'username': username})
                # If user present....
                if(data):
                    collection.delete_one({'username': username})
                    return {'Success': 'Found and deleted User successfully.','user': {'id': data['id'], 'firstName': data['firstName'], 'lastName': data['lastName'], 'username': data['username'], 'email': data['email'], 'password': data['password'], 'address': data['address'], 'mobileNumber': data['mobileNumber']}}
                # If no user present with given username....
                else:
                    return {'Error': 'No such User exists.', 'username': username}
            # If Parameters not specified correctly....
            else:
                return {'Error': {'Parameters not specified correctly.' : 'You need to provide id, email or username.'}}
        # Authentication Error API_KEY Provided is Wrong....
        else:
            return {'Authentication Error': 'SECRET_KEY Provided is Wrong.', 'SECRET_KEY': request.args.get('SECRET_KEY')}
    # Method Error Only post method allowed on this endpoint....
    else:
        return {'Method Error': 'Only post method allowed on this endpoint.', 'request-type': request.method}


# API endpoint to update user from database from backend Mongoose Database and Returning Reposnse Object for CMS platform....
@app.route('/api/v1/update_user', methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
@cross_origin()
def update_user():
    # Table where data is stored....
    collection = db[SECRET_KEY]
    # If Request Method is POST....
    if(request.method=='POST'):
        collection = db[SECRET_KEY]
        # If correct SECRET_KEY passed to the API endpoint....
        if(request.args.get('SECRET_KEY') == SECRET_KEY):
            # Getting id of user to be searched....
            id = request.args.get('id')
            email = request.args.get('email')
            firstName = request.args.get('firstName')
            lastName = request.args.get('lastName')
            username = request.args.get('username')
            password = request.args.get('password')
            address = request.args.get('address')
            mobileNumber = request.args.get('mobileNumber')
            # If Parameters not specified correctly....
            if(id is None or id == ''):
                return {'Error': {'Parameters not specified correctly.' : 'You need to provide id.', 'id': id}}
            elif(email is None or email == ''):
                return {'Error': {'Parameters not specified correctly.' : 'You need to provide email.', 'email': email}}
            elif(firstName is None or firstName == ''):
                return {'Error': {'Parameters not specified correctly.' : 'You need to provide firstName.', 'firstName': firstName}}
            elif(lastName is None or lastName == ''):
                return {'Error': {'Parameters not specified correctly.' : 'You need to provide lastName.', 'lastName': lastName}}
            elif(username is None or username == ''):
                return {'Error': {'Parameters not specified correctly.' : 'You need to provide username.', 'username': username}}
            elif(password is None or password == ''):
                return {'Error': {'Parameters not specified correctly.' : 'You need to provide password.', 'password': password}}
            elif(address is None or address == ''):
                return {'Error': {'Parameters not specified correctly.' : 'You need to provide address.', 'address': address}}
            elif(mobileNumber is None or mobileNumber == ''):
                return {'Error': {'Parameters not specified correctly.' : 'You need to provide mobileNumber.', 'mobileNumber': mobileNumber}}
            # If Parameters specified correctly....
            else:
                collection.update_one({ "id": str(id) }, {'$set': {'id': str(id), 'firstName': str(firstName), 'lastName': str(lastName), 'username': str(username), 'password': str(password), 'email': str(email), 'mobileNumber': str(mobileNumber), 'address': str(address)}})
                return {"Success": 'User updated Successfully.', 'new user':{'id': str(id), 'firstName': str(firstName), 'lastName': str(lastName), 'username': str(username), 'password': str(password), 'email': str(email), 'mobileNumber': str(mobileNumber), 'address': str(address)}}
        # Authentication Error API_KEY Provided is Wrong....
        else:
            return {'Authentication Error': 'SECRET_KEY Provided is Wrong.', 'SECRET_KEY': request.args.get('API_KEY')}
    # Method Error Only post method allowed on this endpoint....
    else:
        return {'Method Error': 'Only post method allowed on this endpoint.', 'request-type': request.method}


#####################################################################################################################
########################################## CMS CLIENT OPERATIONS CRUD API ###########################################
#####################################################################################################################


# API Endpoint for CMS Operations Creating Collection....
@app.route('/api/v1/create_api/dbOp/create_collection', methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
@cross_origin()
def create_api_dbOp():
    userTable = db[SECRET_KEY]
    # If Request Method is POST....
    if(request.method=='POST'):
        API_KEY = request.args.get('API_KEY')
        # If correct API_KEY passed to the API endpoint....
        if(API_KEY is not None and API_KEY != ''):
            # If user exists with API_KEY....
            if(userTable.find_one({'id': API_KEY})):
                # If tableName is not None or emtpy....
                if(request.args.get('tableName') is not None and str(request.args.get('tableName')) != ''):
                    try:
                       # If table exists in database....
                       db.validate_collection(API_KEY+'---'+str(request.args.get('tableName')))
                       return {'Parameter Error': 'Table Name already exists.', 'Table Name': str(request.args.get('tableName'))}
                    except pymongo.errors.OperationFailure:
                        # If table doen't exists in database....
                        db.create_collection(API_KEY+'---'+str(request.args.get('tableName')))
                        return {'Success': 'Table Created successfully.', 'Created': {'Table Name': str(request.args.get('tableName'))}}
                # If no tableName provided....
                else:
                    return {'Parameter Error': 'Please provide tableName.'}
            # If user doen't exists with API_KEY....
            else:
                return {'Authentication Error': 'API_KEY Provided is Wrong.', 'API_KEY': API_KEY}
        # Authentication Error API_KEY Provided is Wrong....
        else:
            return {'Authentication Error': 'API_KEY not provided.', 'API_KEY': API_KEY}
    # Method Error Only post method allowed on this endpoint....
    else:
        return {'Method Error': 'Only post method allowed on this endpoint.', 'request-type': request.method}


# API Endpoint for CMS Operations Deleting Collection....
@app.route('/api/v1/create_api/dbOp/delete_collection', methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
@cross_origin()
def delete_api_dbOp():
    userTable = db[SECRET_KEY]
    # If Request Method is POST....
    if(request.method=='POST'):
        API_KEY = request.args.get('API_KEY')
        # If correct API_KEY passed to the API endpoint....
        if(API_KEY is not None and API_KEY != ''):
            # If user exists with API_KEY....
            if(userTable.find_one({'id': API_KEY})):
                # If tableName is not None or emtpy....
                if(request.args.get('tableName') is not None and str(request.args.get('tableName')) != ''):
                    try:
                       # If table exists in database....
                       db.validate_collection(API_KEY+'---'+str(request.args.get('tableName')))
                       db.drop_collection(API_KEY+'---'+str(request.args.get('tableName')))
                       return {'Success': 'Table Deleted successfully.', 'Deleted': {'Table Name': str(request.args.get('tableName'))}}
                    except pymongo.errors.OperationFailure:
                        # If table doen't exists in database....
                        return {'Parameter Error': "Table doen't exists.", 'tableName': str(request.args.get('tableName'))}
                # If no tableName provided....
                else:
                    return {'Parameter Error': 'Please provide tableName.'}
            # If no user exists with API_KEY....
            else:
                return {'Authentication Error': 'API_KEY Provided is Wrong.', 'API_KEY': API_KEY}
        # Authentication Error API_KEY is not rovided....
        else:
            return {'Authentication Error': 'API_KEY is not provided.', 'API_KEY': API_KEY}
    # Method Error Only post method allowed on this endpoint....
    else:
        return {'Method Error': 'Only post method allowed on this endpoint.', 'request-type': request.method}


# API Endpoint for CMS Operations Editing Collection....
@app.route('/api/v1/create_api/dbOp/edit_collection', methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
@cross_origin()
def edit_api_dbOp():
    userTable = db[SECRET_KEY]
    # If Request Method is POST....
    if(request.method=='POST'):
        API_KEY = request.args.get('API_KEY')
        # If API_KEY passed to the API endpoint....
        if(API_KEY is not None and API_KEY != ''):
            # If correct API_KEY passed to the API endpoint....
            if(userTable.find_one({'id': API_KEY})):
                # If tableName provided....
                if((request.args.get('oldtableName') is not None and str(request.args.get('oldtableName')) != '') and (request.args.get('newtableName') is not None and str(request.args.get('newtableName')) != '')):
                    try:
                       # If table exists in database....
                       db.validate_collection(API_KEY+'---'+str(request.args.get('oldtableName')))
                       db[API_KEY+'---'+str(request.args.get('oldtableName'))].rename(API_KEY+'---'+str(request.args.get('newtableName')), dropTarget = True)
                       return {'Success': 'Table Edited successfully.', 'Changed': {'Table Name': str(request.args.get('newtableName'))}}
                    except pymongo.errors.OperationFailure:
                        # If table doen't exists in database....
                        return {'Parameter Error': "Table doen't exists.", 'oldtableName': str(request.args.get('oldtableName'))}
                # If no tableName provided....
                else:
                    return {'Parameter Error': 'Please provide newtableName and oldtableName.', 'Provide': {'newtableName':str(request.args.get('newtableName')), 'oldtablename':str(request.args.get('oldtableName'))}}
            # If wrong API_KEY passed to the API endpoint....
            else:
                return {'Authentication Error': 'API_KEY Provided is Wrong.', 'API_KEY': request.args.get('API_KEY')}
        # Authentication Error API_KEY Provided is Wrong....
        else:
            return {'Authentication Error': 'API_KEY is not provided is Wrong.', 'API_KEY': request.args.get('API_KEY')}
    # Method Error Only post method allowed on this endpoint....
    else:
        return {'Method Error': 'Only post method allowed on this endpoint.', 'request-type': request.method}


# API Endpoint for CMS Operations Reading Collection....
@app.route('/api/v1/create_api/dbOp/read_collection', methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
@cross_origin()
def read_api_dbOp():
    userTable = db[SECRET_KEY]
    # If Request Method is POST....
    if(request.method=='POST'):
        API_KEY = request.args.get('API_KEY')
        # If API_KEY passed to the API endpoint....
        if(API_KEY is not None and API_KEY != ''):
            # If correct API_KEY passed to the API endpoint....
            if(userTable.find_one({'id': API_KEY})):
                collection = []
                count = 0
                # Lopping through all the collectons in database....
                for i in db.list_collection_names():
                    # If API_KEY present in the collection name....
                    if(i.find(API_KEY) == 0):
                        count+=1
                        # Removing API_KEY and --- from collection name....
                        i = i.replace(API_KEY+"---", '')
                        # Appending it to the collection....
                        collection.append(i)
                # Returing list of collection to the user....
                return {'Found': f'You have {count} collections.', 'collection': f"{collection}"}
            # If wrong API_KEY passed to the API endpoint....
            else:
                return {'Authentication Error': 'API_KEY Provided is Wrong.', 'API_KEY': request.args.get('API_KEY')}
        # Authentication Error API_KEY Provided is Wrong....
        else:
            return {'Authentication Error': 'API_KEY is not provided is Wrong.', 'API_KEY': request.args.get('API_KEY')}
    # Method Error Only post method allowed on this endpoint....
    else:
        return {'Method Error': 'Only post method allowed on this endpoint.', 'request-type': request.method}


# API Endpoint for CMS Operations adding data to the table....
@app.route('/api/v1/create_api/dbOp/add_data', methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
@cross_origin()
def add_data_api_dbOp():
    userTable = db[SECRET_KEY]
    # If Request Method is POST....
    if(request.method=='POST'):
        API_KEY = request.args.get('API_KEY')
        # If API_KEY passed to the API endpoint....
        if(API_KEY is not None and API_KEY != ''):
            # If correct API_KEY passed to the API endpoint....
            if(userTable.find_one({'id': API_KEY})):
                tableName = request.args.get('tableName')
                # If tableName provided....
                if(request.args.get('tableName') is not None and str(request.args.get('tableName')) != ''):
                    try:
                        # If table exists....
                        db.validate_collection(API_KEY+'---'+tableName)
                        data = request.args.get('data')
                        collection = db[API_KEY+'---'+tableName]
                        # If data is provided....
                        if(data is not None and data != '' and data != '{}'):
                            data = f"""{data}""".replace("'", '"')
                            # If json data passed....
                            try:
                                collection.insert_one(json.loads(data))
                                return {'Success': 'Data added to collection successfully.', 'data': str(data)}
                            # If json data not passed....
                            except:
                                return {'Parameter Error': 'data must be a json.', 'data-passed': str(type(data))}
                        # If data is not provided....
                        else:
                            return {'Parameter Error': 'Please provide data.', 'data': data}
                    except pymongo.errors.OperationFailure:
                        # tableName doen't exists....
                        return {'Database Error': 'No such table exists.', 'tableName': tableName}
                # If no tableName provided....
                else:
                    return {'Parameter Error': 'Please provide tableName.', 'Provide': {'tableName':str(request.args.get('tableName'))}}
            # If wrong API_KEY passed to the API endpoint....
            else:
                return {'Authentication Error': 'API_KEY Provided is Wrong.', 'API_KEY': request.args.get('API_KEY')}
        # Authentication Error API_KEY Provided is Wrong....
        else:
            return {'Authentication Error': 'API_KEY is not provided is Wrong.', 'API_KEY': request.args.get('API_KEY')}
    # Method Error Only post method allowed on this endpoint....
    else:
        return {'Method Error': 'Only post method allowed on this endpoint.', 'request-type': request.method}


# API Endpoint for CMS Operations reading all data to the table....
@app.route('/api/v1/create_api/dbOp/read_all', methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
@cross_origin()
def read_all_api_dbOp():
    userTable = db[SECRET_KEY]
    # If Request Method is POST....
    if(request.method=='POST'):
        API_KEY = request.args.get('API_KEY')
        # If API_KEY passed to the API endpoint....
        if(API_KEY is not None and API_KEY != ''):
            # If correct API_KEY passed to the API endpoint....
            if(userTable.find_one({'id': API_KEY})):
                tableName = request.args.get('tableName')
                # If tableName provided....
                if(request.args.get('tableName') is not None and str(request.args.get('tableName')) != ''):
                    try:
                        # If table exists....
                        db.validate_collection(API_KEY+'---'+tableName)
                        collection = db[API_KEY+'---'+tableName]
                        cursor = collection.find({})
                        allData = []
                        for document in cursor:
                            allData.append(str(document))
                        return {'Found': 'Fetched all data from the collection.', 'data': str(allData)}
                    except pymongo.errors.OperationFailure:
                        # tableName doen't exists....
                        return {'Database Error': 'No such table exists.', 'tableName': tableName}
                # If no tableName provided....
                else:
                    return {'Parameter Error': 'Please provide tableName.', 'Provide': {'tableName':str(request.args.get('tableName'))}}
            # If wrong API_KEY passed to the API endpoint....
            else:
                return {'Authentication Error': 'API_KEY Provided is Wrong.', 'API_KEY': request.args.get('API_KEY')}
        # Authentication Error API_KEY Provided is Wrong....
        else:
            return {'Authentication Error': 'API_KEY is not provided is Wrong.', 'API_KEY': request.args.get('API_KEY')}
    # Method Error Only post method allowed on this endpoint....
    else:
        return {'Method Error': 'Only post method allowed on this endpoint.', 'request-type': request.method}


# API Endpoint for CMS Operations reading specific data to the table....
@app.route('/api/v1/create_api/dbOp/read_data', methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
@cross_origin()
def read_data_api_dbOp():
    userTable = db[SECRET_KEY]
    # If Request Method is POST....
    if(request.method=='POST'):
        API_KEY = request.args.get('API_KEY')
        # If API_KEY passed to the API endpoint....
        if(API_KEY is not None and API_KEY != ''):
            # If correct API_KEY passed to the API endpoint....
            if(userTable.find_one({'id': API_KEY})):
                tableName = request.args.get('tableName')
                # If tableName provided....  
                if(request.args.get('tableName') is not None and str(request.args.get('tableName')) != ''):
                    try:
                        # If table exists....
                        db.validate_collection(API_KEY+'---'+tableName)
                        identifier = request.args.get('identifier') 
                        collection = db[API_KEY+'---'+tableName]  
                        # If data is provided....
                        if(identifier is not None and identifier != '' and identifier !='{}'):
                            identifier = f"""{identifier}""".replace("'", '"')
                            try:
                                data = collection.find_one(json.loads(identifier))
                                if(data):
                                    return {'Found': 'Fetched data from the collection.', 'data': str(data)}
                                else:
                                    return {'Database Error': 'No such data exists wrong identifier.', 'identifier': identifier}
                            except:
                                return {'Parameter Error': 'Identifier must be a json.', 'identifier-passed': str(type(identifier))}
                        # If data is not provided....
                        else:
                            return {'Parameter Error': 'Please provide identifier.', 'identifier': identifier}
                    except pymongo.errors.OperationFailure:
                        # tableName doen't exists....
                        return {'Database Error': 'No such table exists.', 'tableName': tableName}
                # If no tableName provided....
                else:
                    return {'Parameter Error': 'Please provide tableName.', 'Provide': {'tableName':str(request.args.get('tableName'))}}
            # If wrong API_KEY passed to the API endpoint....
            else:
                return {'Authentication Error': 'API_KEY Provided is Wrong.', 'API_KEY': request.args.get('API_KEY')}
        # Authentication Error API_KEY Provided is Wrong....
        else:
            return {'Authentication Error': 'API_KEY is not provided is Wrong.', 'API_KEY': request.args.get('API_KEY')}
    # Method Error Only post method allowed on this endpoint....
    else:
        return {'Method Error': 'Only post method allowed on this endpoint.', 'request-type': request.method}


# API Endpoint for CMS Operations Editing data to the table....
@app.route('/api/v1/create_api/dbOp/edit_data', methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
@cross_origin()
def edit_data_api_dbOp():
    userTable = db[SECRET_KEY]
    # If Request Method is POST....
    if(request.method=='POST'):
        API_KEY = request.args.get('API_KEY')
        # If API_KEY passed to the API endpoint....
        if(API_KEY is not None and API_KEY != ''):
            # If correct API_KEY passed to the API endpoint....
            if(userTable.find_one({'id': API_KEY})):
                tableName = request.args.get('tableName')
                # If tableName provided....
                if(request.args.get('tableName') is not None and str(request.args.get('tableName')) != ''):
                    try:
                        # If table exists....
                        db.validate_collection(API_KEY+'---'+tableName)
                        data = request.args.get('newData')
                        collection = db[API_KEY+'---'+tableName]
                        # If data is provided....
                        if(data is not None and data != ''):
                            data = f"""{data}""".replace("'", '"')
                            identifier = request.args.get('identifier')
                            # If identifier is provided....
                            if(identifier is not None and identifier != '' and identifier !='{}'):
                                # If data exists with provided identifier....
                                identifier = f"""{identifier}""".replace("'", '"')
                                # If identifier is json....
                                try:
                                    if(collection.find_one(json.loads(identifier))):
                                        collection.update_many(json.loads(identifier), {'$set': json.loads(data)})
                                        return {'Success': 'Data changed in collection successfully.', 'newData': str(collection.find_one(json.loads(identifier))), 'identifier': identifier}
                                    # If data doen't exists with provided identifier....
                                    else:
                                        return {'Database Error': 'No such data exists wrong identifier.', 'identifier': identifier}
                                # If identifier isn't json....
                                except:
                                    return {'Parameter Error': 'Identifier and data must be a json.', 'identifier-passed': str(type(identifier)), 'data-passed':str(type(data))}
                            # If identifier is not provided....
                            else:
                                return {'Parameter Error': 'Please provide identifier.', 'identifier': identifier, 'Identifier': 'Identifier must be a json with unique key and value.'}
                        # If data is not provided....
                        else:
                            return {'Parameter Error': 'Please provide newData.', 'newData': data}
                    except pymongo.errors.OperationFailure:
                        # tableName doen't exists....
                        return {'Database Error': 'No such table exists.', 'tableName': tableName}
                # If no tableName provided....
                else:
                    return {'Parameter Error': 'Please provide tableName.', 'Provide': {'tableName':str(request.args.get('tableName'))}}
            # If wrong API_KEY passed to the API endpoint....
            else:
                return {'Authentication Error': 'API_KEY Provided is Wrong.', 'API_KEY': request.args.get('API_KEY')}
        # Authentication Error API_KEY Provided is Wrong....
        else:
            return {'Authentication Error': 'API_KEY is not provided is Wrong.', 'API_KEY': request.args.get('API_KEY')}
    # Method Error Only post method allowed on this endpoint....
    else:
        return {'Method Error': 'Only post method allowed on this endpoint.', 'request-type': request.method}


# API Endpoint for CMS Operations deleting specific data to the table....
@app.route('/api/v1/create_api/dbOp/delete_data', methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
@cross_origin()
def delete_data_api_dbOp():
    userTable = db[SECRET_KEY]
    # If Request Method is POST....
    if(request.method=='POST'):
        API_KEY = request.args.get('API_KEY')
        # If API_KEY passed to the API endpoint....
        if(API_KEY is not None and API_KEY != ''):
            # If correct API_KEY passed to the API endpoint....
            if(userTable.find_one({'id': API_KEY})):
                tableName = request.args.get('tableName')
                # If tableName provided....
                if(request.args.get('tableName') is not None and str(request.args.get('tableName')) != ''):
                    try:
                        # If table exists....
                        db.validate_collection(API_KEY+'---'+tableName)
                        identifier = request.args.get('identifier')
                        collection = db[API_KEY+'---'+tableName]
                        # If data is provided....
                        if(identifier is not None and identifier != '' and identifier !='{}'):
                            identifier = f"""{identifier}""".replace("'", '"')
                            try:
                                data = collection.find_one(json.loads(identifier))
                                if(data):
                                    collection.delete_many(json.loads(identifier))
                                    return {'Success': 'Data Deleted from collection successfully.', 'data': str(identifier)}
                                else:
                                    return {'Database Error': 'No such data exists wrong identifier.', 'identifier': identifier}
                            except:
                                return {'Parameter Error': 'Identifier must be a json.', 'identifier-passed': str(type(identifier))}
                        # If data is not provided....
                        else:
                            return {'Parameter Error': 'Please provide identifier.', 'identifier': identifier}
                    except pymongo.errors.OperationFailure:
                        # tableName doen't exists....
                        return {'Database Error': 'No such table exists.', 'tableName': tableName}
                # If no tableName provided....
                else:
                    return {'Parameter Error': 'Please provide tableName.', 'Provide': {'tableName':str(request.args.get('tableName'))}}
            # If wrong API_KEY passed to the API endpoint....
            else:
                return {'Authentication Error': 'API_KEY Provided is Wrong.', 'API_KEY': request.args.get('API_KEY')}
        # Authentication Error API_KEY Provided is Wrong....
        else:
            return {'Authentication Error': 'API_KEY is not provided is Wrong.', 'API_KEY': request.args.get('API_KEY')}
    # Method Error Only post method allowed on this endpoint....
    else:
        return {'Method Error': 'Only post method allowed on this endpoint.', 'request-type': request.method}


#####################################################################################################################
##################################### CMS CLIENT OPERATIONS CRUD API ANALYTICS ######################################
#####################################################################################################################

# Running the app in debug mode....
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
