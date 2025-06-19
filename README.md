# Strivision

A personalized **POTD dashboard** for Striver's A2Z DSA course, helping you track, star, and revisit your daily questions across platforms in a clean, efficient, and user-centric interface.

---

## 🌐 Live Demo

👉 [https://strivision.onrender.com/](https://strivision.onrender.com/) — Explore Strivision live and start practicing!

---

## 🔐 How to Obtain Your Password

Strivision integrates with your credentials from **[takeuforward.org](https://takeuforward.org/)**.

### Existing Users

-  Visit: [https://takeuforward.org/profile/](https://takeuforward.org/profile/)
- Set or reset your password.
- Use that email and password to log into Strivision.

### New Users

- Go to: [https://takeuforward.org/](https://takeuforward.org/)
- Click **Login → Register**, and create your account.
- After registration, go to your profile settings and set a password.

---

## 📌 Features

* Personalized POTD (Problem of the Day) from Striver sheets.
* ⭐ Revisit starred questions to practice and revise.
* 📊 Track solved/unsolved stats across all sheets.
* 📅 Maintain consistency with daily question selection.
* 📱 Responsive UI with intuitive layout.


---

## ⚙️ Local Installation

> Recommended only if you want to run the app on your machine for development/testing.

### Prerequisites

* Python 3.7+
* Flask
* Striver TakeUForward Credentials

### Setup Instructions

```bash
# 1. Clone the repository
$ git clone https://github.com/rampageousrj/strivision.git
$ cd strivision

# 2. (Optional) Create a virtual environment
$ python -m venv venv
$ source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# 3. Install dependencies
$ pip install -r requirements.txt

# 4. Run the Flask app
$ flask run
```

Once running, access the app locally at: [http://localhost:5000](http://localhost:5000)

---

## 🧑‍💻 Usage

* Log in with your email and password as configured via [takeuforward.org](https://takeyouforward.org).
* Use the **Need Help?** popup to access clear login instructions.
* Click the ⭐ to star/unstar any question on the [takeuforward.org](https://takeyouforward.org) website from any sheet and add them to the list of probable starred questions.
* Navigate through the dashboard to track progress, view Daily Problem Of The Day from multiple coding platforms like Leetcode, GeeksForGeeks and HackerEarth and one from your Striver starred questions.

---
