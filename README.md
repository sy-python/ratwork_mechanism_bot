# Ratwork Mechanism
A discord bot created for the Failbetter Games Community discord server.

**Current version:** 1.0.0

## Features

Whenever a user's message amasses enough reactions, the bot will automatically assign them a role that corresponds to the reacted emote.
The user can remove those roles once every week using the `/cleanse` command.

## Requirements

- Python 3.12 or higher
- Packages listed in requirements.txt

## Installation
1. Clone the repository

    ```bash
    git clone https://github.com/sy-python/ratwork_mechanism_bot.git
    ```

2. Create a virtual environment and install dependencies

    ```bash
    python3.12 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Set up environment variables

    Create a `.env` file in the root directory of the repository and add the following lines:

    ```
    DISCORD_TOKEN=(Your Discord bot token)
    SERVER_ID=(The ID of the server you want to run the bot in)
    DATABASE_LOCATION=(The path to the SQLite database file, reccommended to be in the same directory as the bot)
    MENACE_EMOTE_ROLE_MAP=(A JSON string mapping emote IDs to role IDs)
    MENACE_THRESHOLD=(The number of reactions required to trigger a menace)
    ENVIRONMENT=(The environment the bot is running in, either "development" or "production")
    ```

4. Run the bot

    ```bash
    python3.12 ratwork_mechanism_bot/bot.py
    ```

## Contributing
If you would like to contribute to this project, please fork the repository and create a pull request.
Don't forget to format your code with [black](https://black.readthedocs.io/en/stable/).
Each pull request is reviewed by [CodeRabbit](https://github.com/CodeRabbitAI) and manually by [sy-python](https://github.com/sy-python).

## License
This project is licensed under the [MIT License](https://github.com/sy-python/ratwork_mechanism_bot/blob/main/LICENSE.md).

## Acknowledgements
I would like to thank the Failbetter Games Community discord server for giving me the opportunity to create this bot.
