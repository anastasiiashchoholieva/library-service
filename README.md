# Social Media API

 ---
 This Django REST framework-based API serves as a RESTful interface for a library service.

## Installation

 ---

Create venv and install requirements
```
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
```

## Configuration

 ---

### Environment Variables

This project uses environment variables for configuration. To set up the required variables, follow these steps:

1. Create a new `.env` file in the root directory of the project.

2. Copy the contents of the `.env_sample` file into `.env`.

3. Replace the placeholder values in the `.env` file with the actual values specific to your environment.


## Usage

 ---

- To apply migrations to the database use command:
```
python manage.py migrate
```
- Use the following command to load prepared data from fixture:
```
python manage.py loaddata library_service_data.json
```
- After loading data from fixture you can use following test user for login:

Email: `admin@admin.com`
Password: `1qazcde3`

or create one yourself using command:

```
python manage.py createsuperuser
```

- To run server use command:
```
python manage.py runserver
```

 ## Features available

 ---
 * Authentication: Implement a secure method of accessing API endpoints by utilizing JWT token-based authentication.
 * Book management: Enable comprehensive CRUD functionality for Books.
 * User management: Allow users to register, modify their profile details.
 * Borrowing management: Borrowing list and detail endpoints. This also includes filtering of Borrowing List and Return Borrowing functionality
 * Implement sending of notifications in Telegram bot on each Borrowing creation.
 * Implement daily-based function for checking borrowings overdue (Celery). 
 * Implement Stripe Payment Session.
 * Implement Fine Payment for book overdue.
 * API documentation: Utilize Swagger UI to automatically generate interactive API documentation, which facilitates developers in effortlessly exploring and testing the API's endpoints.

 ## API Endpoints

 ---
 The following endpoints are available:

 #### User Registration, Authentication and Following
 * api/user/register: Register a new user by providing an email and password.
 * api/user/token: Receive a token
 * api/user/token/refresh/: Refresh token
 * api/user/token/verify/: Verify token
 * api/user/me/: User information
 
## Documentation

 ---

 * api/doc/swagger/: Documentation using Swagger

![endpoints exept user.png](documentation_images%2Fendpoints%20exept%20user.png)
![user endpoint.png](documentation_images%2Fuser%20endpoint.png)

### To run a periodic task, please, run following commands in 2 separate terminals:

1.
```
docker run -d -p 6379:6379 redis
celery -A library_service worker -l INFO
```
2.
```
celery -A library_service beat -l INFO
```
