# Django Project Installation and Setup

Welcome to the Django project! Follow the steps below to install and set up the project on your local machine.

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.x**: Download and install the latest version of Python from [python.org](https://www.python.org/downloads/).
- **Pip**: The package installer for Python (bundled with Python installation).
- **Virtualenv**: For creating isolated Python environments.
- **Git**: For cloning the project repository.

---

## Installation Steps

### 1. Download and Extract the Project

Download the project zip file from WebifyDev.

Extract the downloaded zip file to your desired location on your local machine.

```bash
# Navigate to the extracted project directory
cd <project-directory>
```

### 2. Create and Activate a Virtual Environment

```bash
# Install virtualenv if not already installed
pip install virtualenv

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install the required packages
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project directory and add the required environment variables. Refer to `.env.example` for the required variables.

### 5. Apply Migrations

```bash
# Run database migrations
python manage.py migrate
```

### 6. Run the Development Server

```bash
# Start the Django development server
python manage.py runserver
```

Open your browser and navigate to `http://127.0.0.1:8000/` to access the project.

---

Follow the prompts to set up the admin user credentials. Once created, you can log in to the admin panel at `http://127.0.0.1:8000/admin/`.

### Current HOD Admin Panel Credentials

- **Email**: admin@gmail.com
- **Password**: admin

## Additional Information

### Creating a Superuser

To access the admin panel, create a superuser:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up the admin user credentials. Once created, you can log in to the admin panel at `http://127.0.0.1:8000/admin/`.

### Testing the Application

Run the tests to ensure the application is working as expected:

```bash
python manage.py runserver
```

---

## Troubleshooting

### Common Issues

1. **Virtual Environment Not Activating:**
   - Ensure you have the correct permissions and the `venv` directory exists.

2. **Dependency Installation Errors:**
   - Check the Python and pip versions. Upgrade if necessary using:
     ```bash
     python -m pip install --upgrade pip
     ```

3. **Database Errors:**
   - Ensure the database service is running and the credentials in the `.env` file are correct.

---

## Contributing

If you'd like to contribute to this project, please follow the standard GitHub workflow:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push them to your fork.
4. Submit a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

Happy coding!
