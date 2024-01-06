# discordbot_up


## Installation notes

Please, use a virtual environment

#### With pip
`python -m venv .venv` to create it
To activate it, either
`./.venv/Scripts/activate` or `source ./.venv/Scripts/activate`

#### Dependency install
From root folder do
`python -m pip install -e .`
Will install the project as `src` so that relative paths can be used
Watch out if you have any other `src` dependencies you might have used for other projects.

## .env
You must have a `.env` file located in the `src` folder with the following variables:
```
TOKEN=<discord token provided by discord.com>
USER=<personal sigarra up>
PASSWORD<person siggara pwd>
DB_PATH=<path to the schedules database>
AUTHOR_IDS=<space separated list with discord ids of the developers (to allow testing of !_author functions)>
```

## Mongo

For the information kept by the bot, a mongo database is used. To run it, you can use docker-compose.

From the root folder, run `docker-compose up` to start the mongo container

The databased used is called `up` and thehe collection used is named `users`. See [users](/src/user.py) for more information.

### Running a mongosh

`docker exec -it discordbot-up-mongodb mongosh` to enter the mongo db shell

`use up` to use the `up` database

`db.users.find()` to see the users collection

## Running the bot

Make sure you have followed the steps above

From the root folder, run `python src/main.py` to start the bot
