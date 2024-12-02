# ELLApp

## Description
ELLApp is a web application designed for interactive English language learning, built using the Django framework. The application offers registered users a personal account, access to statistics, and various training modes. It includes two Django apps: `training` and `users`.

---

## Features
1. **User Registration and Profile Management**:
   - Users must register to access the service.
   - Required fields for registration:
     - First Name and Last Name.
     - Email address.
   - A personal account allows users to:
     - Manage their data and settings in the "Settings" section.
     - Update profile information.

2. **Main Screen**:
   - Provides access to:
     - User statistics.
     - Profile settings.
     - Training mode selection.

3. **Statistics Page**:
   - Displays:
     - Total sessions completed.
     - Sessions completed in each mode.
     - Average scores for each mode.

4. **Training Modes**:
   - **Translation**:
     - Users are given words or sentences to translate into English.
     - The application checks the translation for correctness and grammatical accuracy.
     - Users can skip exercises and view correct translations.
   - **Listening**:
     - Users listen to audio files in English.
     - They write down what they hear, and the application checks for accuracy and grammar.
   - Both modes feature three difficulty levels, each with a limited number of tasks.

---

## Project Structure
### Directories and Key Files
1. **Root Project (`mysite`)**:
   - `settings.py`: Core Django project settings.
   - `urls.py`: Includes routing for `training` and `users` apps.

2. **Apps**:
   - **`training`**:
     - `models.py`: Contains models for exercises, results, and statistics.
     - `views.py`: Handles the logic for training sessions and results.
     - `urls.py`: Routes for training-related pages.
     - Templates:
       - `before_result.html`
       - `display_exercise.html`
       - `results.html`
       - `statistic.html`
       - `training_session.html`
     - Static:
       - JavaScript files (`manage_textarea.js`, `validation.js`).
   - **`users`**:
     - `models.py`: Custom user model extending `AbstractUser`.
     - `views.py`: Handles login, registration, and profile management.
     - `urls.py`: Routes for user-related actions (login, registration, password reset).
     - Templates:
       - `login.html`
       - `profile.html`
       - `register.html`
       - Additional templates for password management:
         - `password_reset_form.html`
         - `password_reset_email.html`
         - `password_reset_done.html`
         - `password_reset_confirm.html`
         - `password_reset_complete.html`
         - `password_change_form.html`
         - `password_change_done.html`

3. **Static Files**:
   - Located in `static/`.
   - Includes CSS, JavaScript, and image files for the application's frontend.

4. **Media Files**:
   - Uploaded by users (e.g., audio tasks for the listening mode).

---

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL
- Django 4.2.6

### Steps
1. Clone the repository:
   git clone <repository_url>
2. Install dependencies:
   pip install -r requirements.txt
3. Configure the database: 
   Update DATABASES in settings.py with your PostgreSQL credentials.
4. Apply migrations:
   python manage.py migrate
5. Run the development server:
   python manage.py runserver
6. Access the application at http://127.0.0.1:8000.

## Usage

### Training Modes
1. Navigate to the training session page.
2. Select a training mode (Translation or Listening) and difficulty level.
3. Complete the exercises.
4. View your results and review incorrect answers.

### User Profile
1. Update your profile information in the "Profile" section.
2. Change your password using the "Change Password" option.

### Statistics
- Track your progress and view average scores for each mode.

---

## Technology Stack
- **Backend**: Django 4.2.6
- **Frontend**: HTML, CSS, JavaScript (Bootstrap 5)
- **Database**: PostgreSQL
- **Authentication**: Django's built-in authentication system with a custom user model.

---

Developed by Escapist_1871

