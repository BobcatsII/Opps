# Opps

Automated Deployment Tool

## Installation

```
# python3 
$ git clone https://github.com/BobcatsII/Opps.git
$ cd Opps
$ /opt/pro/rabbitmq3/sbin/rabbitmq-server >& /dev/null &    # Setup, Start Rabbitmq(version==3.6.15)
$ pipenv install
$ cd PyMySQL                # https://github.com/PyMySQL/PyMySQL 
$ python setup.py install  
$ pipenv shell
$ flask initdb --drop       # Initialize the database.
$ flask init                # Initializing the roles and permissions.
$ nohup celery -A opps.tasks.celery  worker -l debug -f opps/logs/celery/celery_task_`date +%Y%m%d`.log & 
$ gunicorn -w 1 -b 0.0.0.0:5000 wsgi:app
* Running on http://your_ip:8000/
```


