# Bank IAV API

The **`Bank-IAV`** is a robust, scalable backend designed to power banking applications. Built with Flask and employing Flask-Migrate for database schema management, this API supports functionalities such as user registration, authentication, and handling banking transactions.

## **Features**

- **User Registration and Authentication**: Secure signup and login capabilities.
- **Database Version Control**: Utilizes Flask-Migrate for handling database migrations, ensuring consistency across environments.
- **Modular Design**: Structured for scalability with clear separation of concerns (models, controllers, api, services).
- **Comprehensive `.gitignore`**: Keeps the repository clean by excluding unnecessary or sensitive files.

## **Getting Started**

### **Prerequisites**

- **Python (3.10):** The programming language.
- **Flask (3.0.2)**: Serves as the foundational web framework for building the **Bank-IAV API**. Flask is lightweight and modular, making it a good choice for building scalable applications.
- **Flask-Migrate (4.0.5)**: Utilized for handling database migrations. This is crucial in a banking application where the data model may evolve over time, requiring changes to the database schema without loss of data.
- **Flask-SQLAlchemy (3.1.1)**: Offers an ORM layer for interacting with the database, simplifying database transactions and queries.
- **Flask-JWT-Extended (4.6.0)**: Adds support for JWT-based authentication, ensuring secure user authentication and session management.
- **psycopg2-binary (2.9.9)**: Provides PostgreSQL database connectivity, a reliable and powerful database choice for financial applications where transactions and data integrity are critical.
- **python-dotenv (1.0.1)**: Manages environment variables, helping in configuring the application in different environments (development, testing, production) without hard-coding configuration values.
- **SQLite** (for local development)
- **PostgresSQL** (for productin)

### **Installation**

1. **Clone the Repository**

    ```bash
    git clone https://github.com/Hamza-cpp/Bank-IAV.git
    cd Bank-IAV
    ```

2. **Set Up a Virtual Environment**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate # On Windows use `.venv\Scripts\activate`
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Initialize the Database**

    Make sure you have Flask-Migrate initialized and then run:

    ```bash
    flask db upgrade
    ```

    This applies the existing migrations to your database, setting up necessary tables.

5. **Run the Application**

    ```bash
    flask run
    # Or
    python run.py
    ```

### **Project Structure**

```bash

Bank-IAV/
│
├── app/
│   ├── __init__.py                # Initializes the application
│   ├── models/                    # Contains all our SQLAlchemy models
│   │   ├── __init__.py            # Makes models a package
│   │   ├── user.py                # User model
│   │   ├── account.py             # Account model
│   │   ├──transaction.py          # Transaction model
│   │   └── ...
│   │
│   ├── services/                  # Business logic layer
│   │   ├── __init__.py            # Makes services a package
│   │   ├── auth_service.py        # Authentication related operations
│   │   ├── user_service.py        # User management operations
│   │   ├── account_service.py     # Account related operations
│   │   └── ...
│   │
│   ├── api/                       # RESTful API endpoints
│   │   ├── __init__.py            # Makes api a package
│   │   ├── errors.py              # Error handlers for API
│   │   ├── auth.py                # Authentication endpoints
│   │   ├── user.py                # User endpoints
│   │   ├── account.py             # Account endpoints
│   │   └── ...
│   │
│   └── utils/                     # Utility functions
│       ├── __init__.py            # Makes utils a package
│       ├── validators.py          # Request data validation functions
│       └── helpers.py             # Miscellaneous helper functions
│ 
├── migrations/                    # Database migrations
│   ├── versions/                  # Individual migration scripts
│   └── ...
├── tests/                         # Test suite
│
├── .gitignore                     # Specifies intentionally untracked files to ignore
├── config.py                      # Configuration settings
├── run.py                         # Entry point to run the application
├── requirements.txt               # Project dependencies
└── README.md                      # Project documentation (this file)
```

### **Usage**

After running the application, you can interact with it using HTTP requests. For example:

- **Register a New User**

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"username":"john_doe", "email":"john@example.com", "password":"123456"}' http://127.0.0.1:5000/auth/register
    ```

## **Contributing**

We welcome contributions to the **`Bank-IAV`**! If you have suggestions for improvement or want to contribute to the codebase, please feel free to fork the repository and submit a pull request.

## **Acknowledgments**

- Flask for providing a lightweight and powerful web framework.
- Flask-Migrate for making database migrations easy to manage.
