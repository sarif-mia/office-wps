## Table of Contents

1. [Introduction](#officeops-workforce-productivity-suite)
   - [Deployed Website](#deployed-website)
   - [Default Credentials](#default-credentials)
2. [Features](#features)
   - [CEO Features](#ceo-can)
   - [Manager Features](#manager-can)
   - [Employee Features](#employee-can)
3. [Screenshots](#screenshots)
4. [Installation](#installation)
5. [Contributions](#contributions)
6. [License](#license)

# OfficeOps: Workforce Productivity Suite

OfficeOps is a powerful Workforce Productivity Suite built using Django, designed to streamline HR and office management processes within your organization. This project allows CEOs, Managers, and Employees to manage various aspects of HR, including employee information, attendance, feedback, and leave requests.

## Deployed Website

You can access the deployed OfficeOps website at [officeops.onrender.com](https://officeops.onrender.com/).

## Default Credentials

For CEO:
- Email: admin@admin.com

For Manager:
- Email: manager@manager.com

For Employee:
- Email: employee@employee.com

## Features

### CEO Can:

- **Manage Your Team:** CEOs have full control to add, update, and remove Managers and Employees within the organization.

- **Organize Company Structure:** CEOs can create and manage Divisions and Departments to structure the company efficiently.

- **Track Employee Attendance:** Monitor employee attendance to ensure a productive workforce.

- **Engage with Feedback:** Review and respond to feedback from both employees and managers to foster a collaborative workplace.

- **Manage Leave Requests:** Approve or reject leave requests from Managers and Employees, ensuring operational continuity.

### Manager Can:

- **Maintain Attendance:** Managers can record and update employee attendance, making it easier to track team productivity.

- **Handle Salaries:** Add or update salary information for employees, streamlining payroll processes.

- **Apply for Leave:** Managers can request time off and have it reviewed by the CEO.

- **Communicate with CEO:** Managers can share feedback and important information directly with the CEO.

### Employee Can:

- **Check Attendance:** Employees can view their attendance records to stay on top of their work hours.

- **Access Salary Information:** Check salary details for transparency and financial planning.

- **Request Leave:** Submit leave requests to the CEO, ensuring seamless time-off management.

- **Connect with CEO:** Employees can provide feedback and share important concerns with the CEO, fostering a culture of open communication.

#
| Send Notification                            | View Notification                            | View Notification                            |

## Quick Deploy to Render

1. Fork this repository to your GitHub account
2. Go to your Render dashboard: [dashboard.render.com](https://dashboard.render.com)
3. Click "New +" and select "Blueprint"
4. Connect your GitHub repository
5. Click "Apply" - Render will automatically:
   - Create a web service
   - Set up a PostgreSQL database
   - Configure all environment variables
   - Deploy your application

Everything is pre-configured in the `render.yaml` file, including:
- Python version
- Build and start commands
- Database setup
- Environment variables
- Redis cache (optional)
- Region configuration (Singapore)

No additional configuration needed! The deployment will be fully automatic.

## Local Installation

1. Clone the repository:
```bash
git clone https://github.com/sarif-mia/office-wps.git
cd office-wps
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```env
# For SQLite (Development)
DATABASE_URL=sqlite:///db.sqlite3
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# For PostgreSQL (Optional)
# DATABASE_URL=postgres://user:password@localhost:5432/dbname
```

5. Initialize the database:
```bash
# Apply migrations
python manage.py migrate

# Create superuser (CEO account)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Access the application:
- Open your browser and go to `http://127.0.0.1:8000`
- Log in with your superuser credentials

## Production Deployment

For production deployment on Render:

1. Ensure your code is in a GitHub repository
2. Create a new Web Service in Render
3. Connect your GitHub repository
4. Configure the build:
   ```
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn office_ops.wsgi:application
   ```
5. Add environment variables:
   - `DATABASE_URL`: Your PostgreSQL database URL (Render will create this automatically if you add a PostgreSQL database)
   - `SECRET_KEY`: Your Django secret key
   - `DEBUG`: Set to "False"
   - `ALLOWED_HOSTS`: Your render domain (e.g., your-app.onrender.com)

## Database Setup

### Development (SQLite)
- SQLite is configured by default for development
- No additional setup required
- Database file: `db.sqlite3`

### Production (PostgreSQL)
1. Create a PostgreSQL database in Render
2. Render will automatically add the `DATABASE_URL` to your environment variables
3. The application will automatically use the PostgreSQL database in production

## Static Files
- Static files are automatically served by Whitenoise in production
- Run `python manage.py collectstatic` to collect all static files
- No additional configuration needed for Render deployment
5. Configure the database settings in settings.py and run migrations:
```
python manage.py makemigrations main_app
python manage.py migrate
```
6. Create a superuser account:
```
python manage.py createsuperuser
```
7. Start the development server:
```
python manage.py runserver
```
8. Access the admin panel at http://localhost:8000/ and log in with the superuser credentials.

## Contributing

Contributions are welcome! If you'd like to contribute to OfficeOps-WPS, feel free to open a pull request. We value your input and appreciate your help in making the app even better.

## License

This project is licensed under the [MIT License](LICENSE.txt).
