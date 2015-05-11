To run this:
===

- Install the requirements for the requirements: `apt-get install python-dev libxslt-dev libxml2-dev libmysqlclient-dev python python-pip`
- install the python libs in requirements.txt (`pip install -r requirements.txt`)
- make sure that the environment variable SERVER_ENV is set (to DEV). This loads the config file you need.
- rename instance/config-sample.py to instance/config.py and change values inside it
- `python run.py`, you can change the port and IP in config/default.py
