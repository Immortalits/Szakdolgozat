# Webshop_API

### Starting stepps:

install python3, then create a virtualenv, activate, install requirements:

```
virtualenv -p python3 venv;
for Mac:
source venv/bin/activate;
for Windows:
venv\scripts\activate;

pip install -r requirements.txt
```

To run the app, use:

```
flask run
```

For flask_JWT authentication:

Create an environment in Postman with your URL and a jwt_token as variable and
create an 'Authentication' variable in the header of the request and use the value:
```
JWT {{jwt_token}}
```
(Baseline only the DELETE method in the user related request require aithentication)

Generate a database through a GET request, like:
```
{{url}}/products
```

### User related methods:

POST:
```
{{url}}/register

{"username": "webshop", "password": "123456", "password_again": "123456"}
```

To authenticate a User, use POST on...:
```
{{url}}/auth

{"username": "webshop", "password": "123456"}
```

...and use the following script in Postman in the 'Tests' tab of the request 
to set the jwt_token Environment variable for testing:
```
// Response body: JSON value check
pm.test("Access token was not empty", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.access_token).not.eq(undefined)
    // set an environment variable
    pm.environment.set("jwt_token", jsonData.access_token);
});
```
To check the authentication, use the DELETE method on a test user.
(Keep in mind, that their ID will remain and 
their other data will become 'null' in the database!
Requests requiring user ID will return with 'user not found' or 'user does not exist' 
that uses the deleted user' ID!)

To get the names of current users, send a GET request here:
```
{{url}}/users
```

To update a username, send a PUT request here:
```
{{url}}/users/<userID>
```
the BODY of the request should contain the following information:
```
{"username": "nameUpdate"}
```

To update a user' password, send a PUT request here:
```
{{url}}/users/<userID>
```
the BODY of the request should contain the following informations:
```
{"username": "webshop2", "password": "567890", "new_password": "234567", "new_password_again": "234567"}
```

In the following part, the url links and their required BODY 
will be linked one by one with their methods and inputs fields in order:

### Product related methods:

```
POST:

{{url}}/products

{
    "productName": "cheese",
    "price": "200",
    "availability": "true",
    "description": "description"
}

(Description is optional, it can be an empty string or removed entirely, 
but still can be added later if needed through PUT method.)

GET:

{{url}}/products

PUT:

{{url}}/products/<productName>

{
    "productName": "cheese",
    "price": "200",
    "availability": "true",
    "description": "description"
}

(description is optional...)

DELETE:

{{url}}/products/milk
```


### Category related functions:

POST:

{{url}}/categories

{
    "categoryName": "Test"
}

DELETE:

{{url}}/categories/<category_id>

PUT:

{{url}}/categories/<category_id>

{
    "categoryName": "Updated"
}

GET:

{{url}}/categories

to get all products in a specific category:

{{url}}/categories/<category_id>


### Assignments:

```
Product to Category:

POST:

{{url}}/assign

{"product_id": 1, "category_id": 1}

PUT:

{{url}}/assign

{"product_id": 1, "category_id": 1, "new_category_id": 2}

DELETE:

{{url}}/assign

{"product_id": 2, "category_id": 1}
```

```
Product to Cart:

POST:

{{url}}/users/<userID>/cart

{
    "product_id" : 1,
    "user_id": 1,
    "amount": 1
}

(through this request, you can add ur substract amount from the cart 
or even delete, if you substract a high enough number to get the amount lower, than 0)

PUT:

{{url}}/users/<userID>/cart

{
    "product_id" : 1,
    "user_id": 1,
    "amount": 5
}

(to set the amount of a product to a new value)

DELETE:

{{url}}/users/<userID>/cart

{
    "product_id" : 1,
    "user_id": 1,
}

(to remove product from cart)
```

Please report any issues you find by use this API through github, so I can fix them as my time allows!