# Webshop_API


install python3, then create a virtualenv, activate, install requirements:

```
virtualenv -p python3 venv;
for Mac:
source venv/bin/activate;
for Windows:
venv\scripts\activate;


pip install -r requirements.txt
```

run the app:

```
flask run
```

For flask_JWT authentication:

Create an environment in Postman with your URL and a jwt_token as variables.

Generate a database through a GET request, like:
```
{{url}}/products
```

Create a user with POST method on the following link:
```
{{url}}/register
```

with this input in the BODY:
```
{"username": "webshop", "password": "123456"}
```

Use a POST method on the following link:
```
{{url}}/auth
```

with the following input in the BODY:
```
{"username": "webshop", "password": "123456"}
```

use the following script in Postman in the 'Tests' tab:
```
// Response body: JSON value check
pm.test("Access token was not empty", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.access_token).not.eq(undefined)
    // set an environment variable
    pm.environment.set("jwt_token", jsonData.access_token);
});
```

In the following part, the url links and their BODY will be linked one by one with their inputs fields and methods in order:

Product related functions:

```
POST:

{{url}}/products

{
    "productName": "cheese",
    "price": "200",
    "availability": "true",
    "description": "Spicy cheddar cheese with excta flavor"
}

(description is optional, it can be an empty string, but it isn't required to exist either, but can be added later)

GET:

{{url}}/products

PUT:

{{url}}/products/<productName>

{
    "productName": "cheese",
    "price": "200",
    "availability": "true",
    "description": "Spicy cheddar cheese with excta flavor"
}

(description is optional...)

DELETE:

{{url}}/products/milk
```

Category related functions:

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

{{url}}/categories/<category_id>



Assignments:

POST:

Product to Category:
{{url}}/assign

{"product_id": 1, "category_id": 1}

PUT:

{{url}}/assign

{"product_id": 1, "category_id": 1, "new_category_id": 2}

DELETE:

{{url}}/assign

{"product_id": 2, "category_id": 1}

