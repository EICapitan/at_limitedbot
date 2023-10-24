# Limited nEXT Bot

Limited nEXT is a music bot for Discord, part of the 'Limited' bot family. It is written in Python and utilizes the Discord.py 2.0 library along with the Wavelink library for music functionality.

## About

Limited nEXT is one of the bots in the 'Limited' series, which includes:

- [Limited nEXT](https://github.com/at-elcapitan/Limited_Py) (this bot)
- [Limited C/Link](https://github.com/at-elcapitan/Limited-C_Link)
- [Limited jEXT](https://github.com/at-elcapitan/AT-Limited_jEXT)

The bot is designed to provide a seamless music streaming experience on Discord, and it is equipped with features that make it stand out.

## Bot Setup and Usage

To get started with Limited nEXT, follow these steps:

Clone this repository to your local machine using the Git program:

```sh
 git clone https://github.com/at-elcapitan/Limited_Py.git
```

Create a .env file in the bot's directory and fill it with your specific values. The file should follow this pattern:


```yaml
DISCORD_TOKEN =       # Your bot token
PASSWD =              # Lavalink server password
DBHOST =              # URL to your PostgreSQL DB
DBUSER =              # Your PostgreSQL DB username
DBPASS =              # PostgreSQL DB password
SPCLNT =              # Spotify client key
SPSECR =              # Spotify secret
```

With the configuration in place, your bot is now ready to use. Simply run the `run.sh` or `run.bat` file to start it.
