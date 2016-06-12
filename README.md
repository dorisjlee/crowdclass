# Crowdclass
#### Doris Jung-Lin Lee, Joanne Lo, Moonhyok Kim, Eric Paulos 
Crowdclass is a novel method that integrates the learning of advanced scientific concepts with the crowdsourcing microtask of image classification. The system is written in Django 1.9. The Juptyer notebooks used to conduct our analysis is provided in the ``analysis`` folder. 

##Requirements:

- python 2.7
  - comes by default on most systems
  - check installed version with `python -V`
- pip: package manager for python
  - install with `sudo easy_install pip`
- django 1.9
  - install with `sudo pip install django`


## Starting the App

- clone the git repository:
    - e.g. `git clone https://github.com/dorisjlee/crowdclass.git`
- navigate to `/crowdclass/webapp/crowdclass`
- run `python manage.py runserver`
  - open a web browser to `http://localhost:8000`