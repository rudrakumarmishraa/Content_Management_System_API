# Content Management System API
Content Management System API is used to create frontend CMS application on any framework such as React.js and Next.js.
It currently provides operations such as User CRUD for CMS Web Appication and API CRUD for users, which will be further scaled 
to provide analytics on data provided by users.


## Imported packages to be used....

1) We are using Flask package to intialise our app and to create and run server and requests to get HTTP request and its parameter for doing backend operations and sending response.

2) We are using pymongo to access our backend MongoDB database and perform different CRUD operations which is hosted on
Clever-Cloud platform.

3) We are using UUID package to generate random ID's which are used as API_KEY for users for Content Management System.

4) We are using json package to convert Strings into json data or python Dict.


### Initialised App object and other variables essential for app....
app = Flask(__name__)
SECRET_KEY = 'Your SECRET_KEY'


#### Database client and db database object intialized....
DATABASE_URI = 'mongodb://DATABASE_URI'
dbClient = pymongo.MongoClient(DATABASE_URI)
db = dbClient['DATABASE_NAME']


##### Main route of app HomePage of API (/)....
Main route of app contain rendering of a HTML document template and only accepts GET request.

##### API endpoint for creating User (/api/v1/create_user)....
API endpoint for creating User saving it to backend Mongoose Database and Returning Reposnse Object for CMS platform.
Endpoint only accepts POST request and return json data.

##### API endpoint to search User (/api/v1/get_user)....
API endpoint to search user from database from backend Mongoose Database and Returning Reposnse Object for CMS platform.
Endpoint only accepts POST request and return json data.

##### API endpoint to delete User (/api/v1/delete_user)....
API endpoint to delete user from database from backend Mongoose Database and Returning Reposnse Object for CMS platform.
Endpoint only accepts POST request and return json data.

##### API endpoint to update User (/api/v1/update_user)....
API endpoint to update user from database from backend Mongoose Database and Returning Reposnse Object for CMS platform.
Endpoint only accepts POST request and return json data.

##### API Endpoint for CMS Operations (/api/v1/create_api/dbOp/create_collection)....
API Endpoint for CMS Operations Creating Collection.
Endpoint only accepts POST request and return json data.

##### API Endpoint for CMS Operations (/api/v1/create_api/dbOp/delete_collection)....
API Endpoint for CMS Operations Deleting Collection.
Endpoint only accepts POST request and return json data.

##### API Endpoint for CMS Operations (/api/v1/create_api/dbOp/edit_collection)....
API Endpoint for CMS Operations Editing Collection.
Endpoint only accepts POST request and return json data.

##### API Endpoint for CMS Operations (/api/v1/create_api/dbOp/read_collection)....
API Endpoint for CMS Operations Reading Collection.
Endpoint only accepts POST request and return json data.

##### API Endpoint for CMS Operations (/api/v1/create_api/dbOp/add_data)....
API Endpoint for CMS Operations adding data to the table.
Endpoint only accepts POST request and return json data.

##### API Endpoint for CMS Operations (/api/v1/create_api/dbOp/read_all)....
API Endpoint for CMS Operations reading all data to the table.
Endpoint only accepts POST request and return json data.

##### API Endpoint for CMS Operations (/api/v1/create_api/dbOp/read_data)....
API Endpoint for CMS Operations reading specific data to the table.
Endpoint only accepts POST request and return json data.

##### API Endpoint for CMS Operations (/api/v1/create_api/dbOp/edit_data)....
API Endpoint for CMS Operations Editing data to the table.
Endpoint only accepts POST request and return json data.

##### API Endpoint for CMS Operations (/api/v1/create_api/dbOp/delete_data)....
API Endpoint for CMS Operations deleting specific data to the table.
Endpoint only accepts POST request and return json data.
