# Quackers Website Deployment Guide

This guide explains how to deploy the Quackers website on an Ubuntu server using Git, a Python virtual environment, Gunicorn, Nginx, and Supervisor. Follow these steps to replicate the deployment process.

## Prerequisites

- **Server Requirements:**  
  - Ubuntu 24.10 (or a similar release)  
  - SSH access to the server  
  - Sufficient privileges (sudo access)

- **Software Requirements:**  
  - Git  
  - Python 3 (with `venv` module)  
  - pip  
  - Nginx  
  - Supervisor  

- **Domain (Optional):**  
  - A domain name properly pointed to your server’s IP address

## Step-by-Step Deployment

### 1. Connect to Your Server

Log in via SSH:

```bash
ssh user@your_server_ip
```

### 2. Update and Upgrade System Packages

Update package lists and upgrade installed packages:

```bash
sudo apt update
sudo apt upgrade -y
```

If the system suggests a kernel upgrade, reboot the server:

```bash
sudo reboot
```

After rebooting, reconnect via SSH.

### 3. Clone the Repository

Clone the Quackers repository from GitHub and navigate into the project directory:

```bash
git clone https://github.com/FrenchFive/quackers.git
cd quackers
```

### 4. Set Up a Python Virtual Environment

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 5. Install Python Dependencies

Install the required packages using pip:

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create a `.env` file in the project root (or update it if it already exists) with necessary settings. For example:

```ini
FLASK_APP=web/main.py
SECRET_KEY=your_unique_secret_key
# Add other environment variables as needed
```

> **Note:** Setting the `SECRET_KEY` is important to avoid session errors in Flask.

### 7. Test the Flask Application Locally

Before moving to production, test the Flask development server:

```bash
flask run --host=0.0.0.0
```

You should see output similar to:

```
* Serving Flask app 'web/main.py'
* Running on http://127.0.0.1:5000
```

Press `CTRL+C` to stop the server once tested.

### 8. Set Up Gunicorn

Install Gunicorn if not already installed:

```bash
pip install gunicorn
```

Test running the application with Gunicorn:

```bash
gunicorn --bind 127.0.0.1:8000 web.main:app
```

If successful, Gunicorn will start and bind to port 8000.

### 9. Configure Nginx as a Reverse Proxy

#### a. Install Nginx

If Nginx is not already installed:

```bash
sudo apt install nginx -y
```

#### b. Create Nginx Site Configuration

Create a new configuration file for your site:

```bash
sudo nano /etc/nginx/sites-available/quackers
```

Paste a configuration similar to the following (adjust `server_name` accordingly):

```nginx
server {
    listen 80;
    server_name quackers.app;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

#### c. Enable the Site and Test Nginx

Link the configuration into the enabled sites directory:

```bash
sudo ln -s /etc/nginx/sites-available/quackers /etc/nginx/sites-enabled
```

Test the Nginx configuration:

```bash
sudo nginx -t
```

If the test is successful, restart Nginx:

```bash
sudo systemctl restart nginx
```

#### d. Allow HTTP Traffic (if using UFW)

```bash
sudo ufw allow 'Nginx Full'
```

### 10. Configure Supervisor to Manage Gunicorn

Create a Supervisor configuration file to run Gunicorn as a managed process:

```bash
sudo nano /etc/supervisor/conf.d/gunicorn_quackers.conf
```

Insert the following configuration (adjust paths, user, and parameters as needed):

```ini
[program:gunicorn_quackers]
command=/home/your_username/quackers/.venv/bin/gunicorn --bind 127.0.0.1:8000 web.main:app
directory=/home/your_username/quackers
user=your_username
autostart=true
autorestart=true
stderr_logfile=/var/log/gunicorn_quackers.err.log
stdout_logfile=/var/log/gunicorn_quackers.out.log
```

Reload Supervisor and update its configuration:

```bash
sudo supervisorctl reread
sudo supervisorctl update
```

Start (or check the status of) the Gunicorn process:

```bash
sudo supervisorctl start gunicorn_quackers
sudo supervisorctl status
```

### 11. Final Verification

- Visit your domain or server IP in a web browser to verify that the application is accessible.
- Check the logs (both Gunicorn and Nginx) if you encounter any issues.

