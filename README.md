# PWP SPRING 2021
# CryptoMonitoring
# Group information
* Joona Päivärinta, jouka.paivarinta@gmail.com
* Jonne Taipale, jonne.taipale@gmail.com
* Sami Varanka, svaranka@gmail.com

# Documentation
The api documentation is available at [apiary](https://cryptomonitoringapi.docs.apiary.io/).

# Install the dependencies
You need to have [python3](https://www.python.org/downloads/) installed on your system.
It is recommended to create a new  virtual environment for the project. You can install virtualenv module from pip

```
pip install virtualenv
``` 

Once the pip has installed virtualenv, go ahead and create a new virtualenv by typing 

```
virtualenv pwp
```

And activate your virtualenv on **windows** by typing `pwp\Scripts\activate.bat` to the command prompt.

Clone this repository and navigate to it's root folder. Install all the requirements by typing
```
pip install -r requirements.txt
``` 

## On windows

Now in the project's root folder, run the `setup.bat` script. The script setups the flask environment variables and the test database for the API. After that, just type `flask run` to run the flask server. 

Now after you have started the flask server, you can run the GUI client by typing `python cryptomonitor_gui\main.py`, or you can run CLI client by typing `python cryptomonitor\client.py`.
  

# Tests
Pytest is used for testing.
To run the api tests navigate to the root folder and type `pytest tests\api_test.py`.
For database tests type `pytest tests\db_test.py` 
