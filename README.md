# Building a Simple Jenkins CI/CD Pipeline for a Dockerized Flask App
I recently built my first real-world CI/CD pipeline using Jenkins, Docker, and Flask — and I want to share the journey with you.

# What I Wanted to Achieve
Automatically build, test, and deploy a Flask app every time I push code
* Use Jenkins for automation
* Containerize the app with Docker
* Run everything on my local machine

# How I Did It
1. Set up the project
Created a basic Flask app and wrote tests using pytest. I also added a requirements.txt file listing dependencies.

2. Created a Jenkinsfile pipeline
Defined stages:

* Clone the GitHub repo
* Install dependencies (pip install -r requirements.txt)
* Run tests (pytest)
* Build Docker image
* Run Docker container

3. Installed Jenkins and Docker on my RHEL machine
Made sure Jenkins can run Docker commands (added Jenkins user to Docker group).
4. Pushed the code to GitHub
Hosted the repo publicly to make integration easier.
5. Connected Jenkins with GitHub using Webhooks and Ngrok
Since Jenkins runs locally, I used ngrok to expose my localhost to the internet. This allowed GitHub to notify Jenkins instantly when I push changes.
6. Configured Jenkins job to trigger on webhook events
Enabled GitHub hook trigger for GITScm polling in Jenkins.

# Challenges I Faced
* Git clone error — Jenkins couldn't find the repo initially because I pointed it to a local folder instead of the GitHub URL.

* pytest not found — Jenkins didn't have pytest installed by default. Fixed by adding pytest to requirements.txt and installing dependencies in the pipeline.

* Python import errors — Tests couldn’t find my Flask app modules because PYTHONPATH wasn’t set. Added export PYTHONPATH=$PWD before running tests.

* Werkzeug version incompatibility — Tests failed with AttributeError: module 'werkzeug' has no attribute '__version__'. Fixed by pinning Werkzeug to a version below 3.0 in requirements.txt.

* Local Jenkins not reachable from GitHub — Solved by using ngrok to create a public tunnel to my localhost.
# The Outcome

Now, every time I push code to GitHub:

* Jenkins automatically clones the repo
* Installs dependencies
* Runs tests
* Builds a Docker image
* Runs the Flask app in Docker
* All without me clicking a button. It’s a fully automated pipeline on my local machine!

# Why This Matters
This project taught me how real CI/CD pipelines work in practice — and gave me a solid foundation to build more advanced DevOps skills. If you're starting your DevOps journey, I recommend building a similar pipeline. It covers all core concepts and tools without being overwhelming.
