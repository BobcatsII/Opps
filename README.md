# Opps

Automated Deployment Tool

## Installation

```
$ git clone https://github.com/BobcatsII/Opps.git
$ cd Opps
$ pipenv install
$ pipenv shell
$ flask initdb --drop   # Initialize the database.
$ flask init            # Initializing the roles and permissions.
$ nohup celery -A opps.tasks.celery  worker -l debug -f opps/logs/celery/celery_task.log & 
$ flask run --host='0.0.0.0' --port='8000'
* Running on http://127.0.0.1:8000/
```


