# Secure Banking System

A secure web-based banking application developed using Python, Flask, SQLAlchemy, Bootstrap, SQLite, and Pytest.

The system allows customers to create accounts, log in securely, transfer money between bank accounts, view transaction history, manage their profiles, and change their passwords.

The system also provides an administrator panel for managing users, bank accounts, and financial transactions.

---

## Project Features

### Customer Features

- Create a new user account
- Automatic bank account creation
- Secure login and logout
- View account number
- View current account balance
- Transfer money to another bank account
- View complete transaction history
- View the latest five transactions
- View personal profile
- Edit username and email address
- Change account password
- Display sent and received transactions separately
- Prevent transfers to the same account
- Prevent transfers that exceed the available balance

### Administrator Features

- View all registered users
- View all bank accounts
- View all financial transactions
- View the total number of users
- View the total number of accounts
- View the total number of transactions
- View the total money stored in bank accounts
- Disable customer accounts
- Enable disabled customer accounts
- Delete customer accounts
- Prevent the administrator from deleting their own account
- Prevent the administrator from disabling their own account
- Protect the administrator page from unauthorized users

---

## Security Features

The project includes several security controls:

- Password hashing using Flask-Bcrypt
- Strong password validation
- Minimum password length requirement
- Uppercase letter requirement
- Lowercase letter requirement
- Number requirement
- Special character requirement
- CSRF protection using Flask-WTF
- User authentication using Flask-Login
- Role-based access control
- Administrator authorization
- Rate limiting for login attempts
- Rate limiting for registration attempts
- Rate limiting for transfer attempts
- Rate limiting for password change attempts
- Prevention of duplicate usernames
- Prevention of duplicate email addresses
- Prevention of disabled-user login
- Input validation
- Account-number validation
- Transfer-amount validation
- Prevention of negative transfers
- Prevention of zero-value transfers
- Prevention of transfers with more than two decimal places
- Database rollback when an error occurs
- Custom error pages
- Secure session configuration
- Database files excluded from GitHub
- Environment files excluded from GitHub

---

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Bcrypt
- Flask-WTF
- Flask-Limiter
- SQLAlchemy
- SQLite
- HTML
- CSS
- Bootstrap
- Jinja2
- Pytest
- Git
- GitHub

---

## Project Structure

`text
secure_Banking_System_pro/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── account.py
│   │   │   └── transactions.py
│   │   │
│   │   ├── routes/
│   │   │   ├── home.py
│   │   │   ├── auth.py
│   │   │   ├── dashboard.py
│   │   │   ├── transfer.py
│   │   │   ├── transactions.py
│   │   │   └── admin.py
│   │   │
│   │   ├── security/
│   │   │   ├── hashing.py
│   │   │   └── validation.py
│   │   │
│   │   ├── services/
│   │   ├── static/
│   │   │   └── css/
│   │   │       └── style.css
│   │   │
│   │   ├── templates/
│   │   │   ├── base.html
│   │   │   ├── home.html
│   │   │   ├── login.html
│   │   │   ├── register.html
│   │   │   ├── dashboard.html
│   │   │   ├── transfer.html
│   │   │   ├── transactions.html
│   │   │   ├── admin.html
│   │   │   ├── profile.html
│   │   │   ├── edit_profile.html
│   │   │   ├── change_password.html
│   │   │   ├── 403.html
│   │   │   ├── 404.html
│   │   │   ├── 429.html
│   │   │   └── 500.html
│   │   │
│   │   ├── extensions.py
│   │   └── init.py
│   │
│   ├── instance/
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
│
├── tests/
│   ├── init.py
│   ├── conftest.py
│   ├── test_pages.py
│   ├── test_auth.py
│   └── test_transfer.py
│
├── database/
├── docker/
├── docs/
├── frontend/
├── .github/
├── .gitignore
├── LICENSE
└── README.md

---

## Database Models

### User Model

The user model stores:

- User ID
- Username
- Email address
- Password hash
- User role
- Account status
- Creation date

### Account Model

The account model stores:

- Account ID
- Account number
- Account balance
- User ID

### Transaction Model

The transaction model stores:

- Transaction ID
- Sender account ID
- Receiver account ID
- Transfer amount
- Transaction date

---

## Application Pages

The main application pages are:

text
/

Home page.

text
/register

User registration page.

text
/login

User login page.

text
/dashboard

Customer dashboard.

text
/transfer

Money transfer page.

text
/transactions

Transaction history page.

text
/profile

User profile page.

text
/profile/edit

Profile editing page.

text
/change-password

Password change page.

text
/admin

Administrator dashboard.

---

## Installation

### 1. Download or clone the project

powershell
git clone <repository-url>

Open the project directory:

powershell
cd secure_Banking_System_pro

### 2. Open the backend directory

powershell
cd backend

### 3. Create a virtual environment

powershell
python -m venv venv

### 4. Activate the virtual environment

For Windows PowerShell:

powershell
.\venv\Scripts\Activate.ps1

For Windows Command Prompt:

cmd
venv\Scripts\activate

### 5. Install the required packages

powershell
python -m pip install -r requirements.txt

---

## Running the Application

Make sure the Terminal is inside the backend directory:

text
secure_Banking_System_pro\backend

Run the application:

powershell
python run.py

The application will run at:

text
http://127.0.0.1:5000

Open this address in a web browser.

---

## Running Automated Tests

The automated tests are located inside the `tests` directory.

Move to the main project directory:

powershell
cd ..

The Terminal path should be:

text
secure_Banking_System_pro

Run all tests:

powershell
python -m pytest tests -v

Current test result:

text
25 passed

---

## Test Coverage

The automated tests cover the following areas:

### Page Tests

- Login page opens correctly
- Registration page opens correctly
- Unknown pages return a 404 response
- Dashboard requires authentication
- Transfer page requires authentication
- Transactions page requires authentication
- Profile page requires authentication
- Change-password page requires authentication
- Administrator page requires authentication

### Authentication Tests

- Registration creates a new user
- Registration creates a bank account automatically
- Duplicate usernames are rejected
- Duplicate email addresses are rejected
- Weak passwords are rejected
- Password confirmation is validated
- Correct login details are accepted
- Incorrect passwords are rejected
- Unknown usernames are rejected
- Disabled users cannot log in

### Transfer Tests

- Successful transfers update the sender balance
- Successful transfers update the receiver balance
- Successful transfers create transaction records
- Transfers to the same account are rejected
- Transfers exceeding the balance are rejected
- Negative transfers are rejected
- Zero-value transfers are rejected
- Unknown receiver accounts are rejected
- Amounts with more than two decimal places are rejected

---

## Running a Specific Test File

Run page tests:

powershell
python -m pytest tests/test_pages.py -v

Run authentication tests:

powershell
python -m pytest tests/test_auth.py -v
`

Run transfer tests:
python -m pytest tests/test_transfer.py -v
---

## Saving Test Results

To save test results in a UTF-8 file using PowerShell:

python -m pytest tests -v 2>&1 | Out-File -FilePath .\pytest_results.log -Encoding utf8
The result will be stored in:

pytest_results.log
---

## Error Pages

The system includes custom pages for the following errors:

### 403 — Access Denied

Displayed when a user attempts to access a page without the required permission.

### 404 — Page Not Found

Displayed when the requested page does not exist.

### 429 — Too Many Requests

Displayed when the user exceeds the permitted number of attempts.

### 500 — Internal Server Error

Displayed when an unexpected internal application error occurs.

---

## Important Security Notes

- Do not upload the SQLite database to GitHub.
- Do not upload the virtual environment.
- Do not upload the .env file.
- Do not store plain-text passwords.
- Do not publish secret keys.
- Disable debug mode before production deployment.
- Use HTTPS in production.
- Use a production database such as PostgreSQL for a real deployment.
- Keep all Python packages updated.
- Use secure environment variables for sensitive configuration.

---

## Git Ignore

The .gitignore file prevents Git from uploading:

- Virtual environment files
- SQLite database files
- Flask instance files
- Environment-variable files
- Python cache files
- Pytest cache files
- Log files
- Temporary files
- IDE configuration files

---

## Project Status

The main backend functions are complete.

Completed components:

- Registration
- Login
- Logout
- Customer dashboard
- Bank-account creation
- Money transfers
- Transaction history
- Profile page
- Profile editing
- Password changing
- Administrator dashboard
- User disabling and enabling
- Customer deletion
- Custom error pages
- Input validation
- Password hashing
- Rate limiting
- CSRF protection
- Automated tests

Automated test result:

25 passed
---

## Future Improvements

Possible future improvements include:

- Email verification
- Password-reset emails
- Two-factor authentication
- Account-freezing feature
- Transaction descriptions
- Bank-statement export
- PDF statement generation
- Search and filtering
- Pagination
- PostgreSQL support
- Docker deployment
- GitHub Actions
- REST API
- Audit logging
- Transaction notifications
- Improved user-interface design

---

## Author

Developed as a Secure Software Development course project.

---

## License

This project is created for educational purposes.