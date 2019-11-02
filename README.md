# AnonSend
An anonymous file sharing service
Way to setup Django project with nginx + gunicorn (python 3 and Django > 2.0) Ubuntu,

1. sudo apt-get update
   sudo apt-get install python3-pip python3-dev libpq-dev nginx
2. To get the other requirments of the project ready, We would recommend to use a virtual enviroment 
   sudo -H pip install --upgrade pip
   sudo -H pip install virtualenv
3. Make a new directory or git clone [your exixting repo]
4. Go to your directory by cd /yourproject
   Now we create a virtual Enviroment
   virtualenv yourenv
   If python3 is the only python version on your system the enviroment will be made by python3 
   else your need to specify the path of the python version you want the virtual enviroment to be
   virtualenv -p /path/to/any/bin/python yourenv
   This will create a directory called yourenv within yourproject directory.
   We can use this to install and configure
5. source yourporject/bin/activate (to activate virtualenv)
   pip install django gunicorn (Regardless Python version you are using, when in virtual environment  
                                          you should use the pip command not 'pip3'
6. Adjusting Project Settings
   Start by Changing the ALLOWED_HOSTS settings , this list tells the django instance about the host that can connect
   nano ~/yourproject/yourporject/settings.py
   ALLOWED_HOSTS = ['your_IP_or_domain', '.example.com', . . .]
7. Check the static files directory settings so that Nginx can handle these requests 
   STATIC_URL = '/static/'
   STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
8. Now its time to makemigrations so that Django can make nesscerry migrations based on models into your database
   python manage.py makemigrations
   python manage.py migrate         *which is responsible for applying and unapplying migrations.
   Make sure from step 5 you are in your virtualenv
   Now we collect all the static content in the directory we configured above
   python manage.py collectstatic
9. At this step your are basically done with your Django app only thing left is firewall rules and Nginx setup
   Create  firewall rule for port:8000 (can be anything your desire)
   Now we test the django application by running the server
   python manage.py runserver 0.0.0.0:8000  *this will run the server on port 8000 the ip will be the static ip of the server
   you can check the app in your web browser by
   http://your_domain_or_IP:8000
   If everything works as intended your will see ur index page or the default index djnago page
   Ctrl+c to exit server
   In production it is recommended to serve the application by a server not django's internal server
   The Gunicorn "Green Unicorn" is a Python Web Server Gateway Interface HTTP server
   gunicorn uses the WSGI application 
   
   WSGI: A Python spec that defines a standard interface for communication between an application or 
   framework and an application/web server. This was created in order to simplify and standardize 
   communication between these components for consistency and interchangeability. This basically defines 
   an API interface that can be used over other protocols. To learn more click https://vsupalov.com/what-is-gunicorn/ ,
                                                            https://www.fullstackpython.com/green-unicorn-gunicorn.html
10.Test gunicorn's ability to serve
   gunicorn --bind 0.0.0.0:8000 myproject.wsgi
   This will start Gunicorn on the same config that the Django development server was running on.
   ctrl-c to quit
   now we can deactivate the virtualenv by using the below command
   deactivate
11.Now we create gunicorn system file which will take the role of starting the app 
   sudo nano /etc/systemd/system/gunicorn.service
   Add the contents below the  dashed-line------------------------------------------------------------
   
   [Unit]
   Description=gunicorn daemon
   After=network.target

   [Service]
   User=yourubuntuusername
   Group=www-data
   WorkingDirectory=/home/yourubuntuusername/yourproject
   ExecStart=/home/yourubuntuusername/yourproject/yourenv/gunicorn --access-logfile - --workers 3 --bind unix:/home/yourubuntuusername/yourproject/yourproject.sock yourproject.wsgi:application

   [Install]
   WantedBy=multi-user.target
  
   END---------------------------------------------------------------------------------------------------
   
    Service file is complete save and close it now.
    now lets start the service
    sudo systemctl start gunicorn
    sudo systemctl enable gunicorn
    To check if the configuration is correct we can check the presence of .sock file (socket)
    ls /home/yourubuntuuser/yourproject
    sudo systemctl status gunicorn --to check the gunicorn status
    If the status inticate an error check the gunicorn logs 
    sudo journalctl -u gunicorn
    If you make changes to the /etc/systemd/system/gunicorn.service run the following commands it is required to do this
    sudo systemctl daemon-reload
    sudo systemctl restart gunicorn
 12.After setting up gunicorn now we nned to setup Nginx to route the traffic
    sudo nano /etc/nginx/sites-available/yourproject
    Add the contents below the  dashed-line------------------------------------------------------------
    server {
    listen 80;
    server_name _domain_or_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/yourubuntuuser/yourproject;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/yourubuntuuser/yourproject/yourproject.sock;   
          }
     }
    END---------------------------------------------------------------------------------------------------
    save and close the file when you are finished
 13.Link the above file
    sudo ln -s /etc/nginx/sites-available/yourproject /etc/nginx/sites-enabled
    Test Nginx config 
    sudo nginx -t
    If no errors restart the server by typing
    sudo systemctl restart nginx
 14.Now we need to traffic are contents to port 80 insted to 8000'
    Delete the previously created open port
    sudo ufw delete allow 8000
    Allow Nginx full control 
    sudo ufw allow 'Nginx Full'

    Configuration of SSl
  1.
    


   
   


  
   

   
   
   

   
   
