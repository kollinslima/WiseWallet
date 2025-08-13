# Wise Wallet

wise-wallet is a web application to manage personal finances.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Python 3.9+
* pip

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd wise-wallet
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
   For Windows, use `venv\Scripts\activate`.

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the database migrations:
    ```bash
    python manage.py migrate
    ```

## Configuration

The application uses a `.env` file for configuration. A `.env.example` file is provided with all the available variables.

1. Create a `.env` file by copying the example:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and set the following variables:

   - `SECRET_KEY`: A secret key for a particular Django installation. You can generate one using the following command:
     ```bash
     python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
     ```
   - `DEBUG`: Set to `True` for development and `False` for production.
   - `DB_ENGINE`: Database engine. Defaults to `django.db.backends.sqlite3`.
   - `DB_NAME`: Database name. Defaults to `db.sqlite3`.
   - `DB_USER`: Database user.
   - `DB_PASSWORD`: Database password.
   - `DB_HOST`: Database host.
   - `DB_PORT`: Database port.
   - `EMAIL_BACKEND`: Email backend. Defaults to `django.core.mail.backends.console.EmailBackend`.
   - `EMAIL_HOST`: Email host.
   - `EMAIL_PORT`: Email port.
   - `EMAIL_USE_TLS`: Whether to use TLS.
   - `EMAIL_HOST_USER`: Email host user.
   - `EMAIL_HOST_PASSWORD`: Email host password.

## Usage

To run the development server, use the following command:
```bash
python manage.py runserver
```
The application will be available at `http://127.0.0.1:8000/`.

## Running the tests

To run the unit tests, use the following command:
```bash
python manage.py test
```
