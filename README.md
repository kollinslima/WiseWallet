# WiseWallet

WiseWallet is a portfolio manager application built with Django. It helps you track your assets and transactions.

## Features

*   **Dashboard:** View a summary of your portfolio.
*   **Transaction Management:** Add, edit, and view your transactions.
*   **Portfolio Tracking:** See the value of your assets over time.

## Prerequisites

*   Python 3.8+
*   pip

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/username/wisewallet.git
    cd wisewallet
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory of the project by copying the example file:
    ```bash
    cp .env.example .env
    ```
    Open the `.env` file and add the following environment variables.
    You will need to generate a secret key. You can use the following command to generate one:
    ```bash
    python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
    ```

    Your `.env` file should look like this:
    ```
    SECRET_KEY=your-secret-key-here
    DEBUG=True
    ```

5.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

## Running the Application

To run the development server, use the following command:
```bash
python manage.py runserver
```
The application will be available at `http://127.0.0.1:8000/`.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
