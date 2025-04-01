Here’s a comprehensive `README.md` file for your **Fitness Social App** project. It includes all the necessary details about the app, its features, setup instructions, and usage.

---

# **Fitness Social App**

A Django-based social fitness platform for connecting users with similar fitness goals, tracking progress, sharing workout plans, and engaging in a community of fitness enthusiasts.

---

## **Features**
 
### **1. User Authentication**
- Sign Up
- Login/Logout
- Profile creation and management

### **2. Dashboard**
- Progress tracker with charts (powered by Chart.js)
- Summary of workouts completed in the last 30 days
- Quick workout logging
- Upcoming workouts
- Recent activity feed from friends

### **3. Workout Plans**
- Create, edit, delete workout plans
- View all workout plans
- Assign workout plans to specific users

### **4. Social Feed**
- Create posts with text and images
- Like and comment on posts
- View posts from users you follow

### **5. Discover People**
- Find users with similar fitness goals or workout plans
- Follow/unfollow users
- View user profiles

---

## **Technologies Used**

### **Backend**
- Django 4.x (Python Web Framework)
- SQLite (Default database for development)

### **Frontend**
- HTML5/CSS3
- Bootstrap 4 for responsive design
- Chart.js for progress tracking visualizations

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/fitness-social-app.git
cd fitness-social-app
```

### **2. Create a Virtual Environment**
Using Conda:
```bash
conda create -n fitness_app python=3.10 -y
conda activate fitness_app
```

Or using `venv`:
```bash
python -m venv env
source env/bin/activate  # On Linux/MacOS
env\Scripts\activate     # On Windows
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Apply Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **5. Create a Superuser**
```bash
python manage.py createsuperuser
```
Follow the prompts to set up an admin account.

### **6. Run the Development Server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## **Usage Instructions**

### **1. Sign Up and Login**
Navigate to `/signup/` to create an account.

### **2. Dashboard**
After logging in, visit `/dashboard/` to:
- View progress stats and charts.
- Log completed workouts.
- See upcoming workouts and recent activity.

### **3. Workout Plans**
Navigate to `/workout-plans/` to:
- Create new workout plans.
- Edit or delete existing plans.

### **4. Social Feed**
Visit `/social-feed/` to:
- Create posts.
- Like and comment on posts from users you follow.

### **5. Discover People**
Navigate to `/discover/` to:
- Find users with similar interests.
- Follow/unfollow users.
- View user profiles.

---

## **Folder Structure**

```
fitness_social_app/
├── core/
│   ├── admin.py          # Admin configurations for models
│   ├── apps.py           # App configuration file
│   ├── forms.py          # Custom forms for workouts, progress, etc.
│   ├── models.py         # Database models for workouts, posts, etc.
│   ├── signals.py        # Automatic profile creation for new users
│   ├── urls.py           # App-level URL routing
│   ├── views.py          # Business logic for views like dashboard, signup, etc.
├── templates/
│   ├── base.html         # Main template with navigation bar and footer
│   ├── dashboard.html    # Dashboard page template with charts and quick log form
│   ├── discover_users.html  # Discover people page template
│   ├── registration/
│   │   ├── login.html    # Login page template
│   │   ├── logout.html   # Logout confirmation page template
│   │   └── signup.html   # Sign-up page template for user registration
├── static/
│   ├── css/              # Custom CSS files (e.g., styles.css)
│   ├── js/               # Custom JavaScript files (e.g., scripts.js)
├── db.sqlite3            # SQLite database file (default development database)
├── manage.py             # Django project management script
├── requirements.txt      # List of dependencies to install via pip
└── settings.py           # Project-level settings file (inside `fitness_social_app`)
```

---

## **Key Features in Detail**

1. ### **Authentication System**
    - Users can sign up, log in, and log out securely.
    - Profiles are automatically created using Django signals.

2. ### **Dashboard Features**
    - Visual progress tracker using Chart.js.
    - Quick workout logging form.
    - Summary of recent activity and upcoming workouts.

3. ### **Workout Plans Management**
    - Full CRUD functionality for workout plans.
    - Assign workouts to specific dates or users.

4. ### **Social Feed Features**
    - Users can create posts with text/images.
    - Like and comment on posts from connections.

5. ### **Discover People Features**
    - Find users based on shared fitness goals or workout plans.
    - Follow/unfollow functionality directly from the Discover page.

---

## Future Enhancements

1. Add notifications for milestones achieved (e.g., "100 workouts completed").
2. Implement a leaderboard feature based on user activity.
3. Support video uploads in social feed posts.
4. Add advanced filtering options in Discover People (e.g., location-based).

---

## License

This project is licensed under the MIT License.

