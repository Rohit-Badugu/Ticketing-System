# Ticketing-System 📈
Ticketing system is a dashboard tool for viewing your tickets in the Zendesk system. It uses Zendesk APIs to fetch the data and is built using Python Flask webframework.

## User Stories :dart:
The below user stories are implemented.

:white_check_mark: Display all the tickets for a user account in a list. <br />
:white_check_mark: User can navigate into individual ticket details. <br />
:white_check_mark: Paging through tickets when more than 25 are returned. <br />
:white_check_mark: Error pages are added to handle a scenario where Zendesk APIs are unavailable or if there is a program error. <br />

## Video Walkthrough :clapper:

Here's a walkthrough of implemented user stories:

<img src='walkthrough.gif' title='Video Walkthrough' width='' alt='Video Walkthrough' />

GIF created with [GIF Maker, GIF Editor](https://play.google.com/store/apps/details?id=com.media.zatashima.studio&hl=en_US&gl=US).

## Getting Started 💻

### Clone the Repository 

Get started by cloning the project to your local machine:

```
$ https://github.com/Rohit-Badugu/Ticketing-System.git
```

### Installation
```requirements.txt``` file contains a list of all the dependencies. 
1. Install `Python3` using the [documentation](https://www.python.org/downloads/). Set the environmenet variables to Python path.
2. Install `pip` tool using the [documentation](https://pip.pypa.io/en/stable/installation/).
3. Install all the dependencies using `pip`. Run the below command
```
$ pip install -r requirements.txt
```

### Usage
#### Configuration
In `config.py` on line 6, enter the Base64 encoded API KEY value

#### Running the server
1. Navigate to repository directory in the terminal. Run the `run.py` python file using below command
```
$ python run.py
```
2. Once the server has started, you can view the localhost URL. The applciation will start on default URL - `http://127.0.0.1:5000/`
3. Open the above URL in a browser to view the application.

#### Running the tests
1. Python `unittest` module is used for writing the unit tests. Unit tests are placed under directory - `tests/unit`.
2. Python `pytest` module is used for writing the functional tests. Functional tests are placed under directory - `tests/functional`.
3. To start the tests, run the below command in the project repository.
```
$ python -m pytest
```

## Functionality :rocket:
### Pagination
### Error Handling

