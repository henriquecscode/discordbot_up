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
```
TOKEN=<discord token provided by discord.com>
USER=<personal sigarra up>
PASSWORD<person siggara pwd>
DB_PATH=<path to the schedules database>