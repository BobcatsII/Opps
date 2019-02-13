# Opps

Automated Deployment Tool

## Installation

```
-- Use python3 --
$ git clone https://github.com/BobcatsII/Opps.git
$ cd Opps
$ pipenv install
$ cd PyMySQL                #https://github.com/PyMySQL/PyMySQL 
$ python setup.py install  
$ pipenv shell
$ flask initdb --drop       # Initialize the database.
$ flask init                # Initializing the roles and permissions.
-- Supervisord setup/usage please view the file supervisor/Readme.txt --
$ supervisord -c /etc/supervisor/supervisord.conf  # Start opps/celery/rabbitmq with supervisor
-- View the supervisor web page
* http://your_ip:9001

* Running on http://your_ip:8000/ view project page
```
