# Over The Mood

## Description

Over The Mood's main feature allows users to keep a log of moods and associated activities. Users are also able to view how their mood fluctuates over time and save journal entires to their profile. Over The Mood was made with the intention of helping others become more self aware of how their actions can influence their emotions.

## How It Works

Upon registering, users will be prompted to add an entry which includes a mood and any number of selected activities from a form. If a user entered a negative mood- they will be prompted to fill out three ways that would enhance their mood and save it to their profile. Users are then able to view a log of all their entires and two visualizations- one for mood over time and another for total mood count. Users are also able to view the activities associated with specfic moods. Lastly, users are able to navigate to a journal entry page where they can dump their feelings, have it analyzed by a sentiment analyzer and later save them to their profile.

## Technology Stack

Application: Python, Flask, Jinja, SQLAlchemy, PostgreSQL <br>
API: Indico Sentiment Analysis <br>
Front-End: HTML/ CSS, Bootstrap, jQuery, JavaScript, React, AJAX

## Getting Started

These instructions will get you a copy of the project up and running on your local machine. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Please be sure to have Python 3.6 and PostgreSQL downloaded before you clone this repository.

### Installing

To run Over The Mood on your local computer, please follow the below steps:

Create an OverTheMood folder and clone repository in folder:

```
git clone https://github.com/lizlaw13/final-project.git
```

Create a virtual environment:

```
virtualenv env
```

Install dependencies:

```
$ pip3 install -r requirements.txt
```

Create database:

```
$ createdb tracker
```

Build database tables and fill database with seed file:

```
$ python3 model.py
$ python3 seed.py
```

Run Over The Mood via the command line:

```
$ python3 server.py
```

Open your browser and navigate to:

```
http://localhost:5000/
```

# Usage

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

- [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
- [Maven](https://maven.apache.org/) - Dependency Management
- [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

- **Billie Thompson** - _Initial work_ - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

- Hat tip to anyone whose code was used
- Inspiration
- etc
