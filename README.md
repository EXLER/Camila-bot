<p align="center">
    <img src="resources/logo.png" width="400">
    <p align="center">🎓 Extensible Discord bot with handful of functionalities for every student!</P>
</p>

## Requirements
* Python 3.8
* ffmpeg

## Usage
* Create a new bot on [Discord Developer Portal](https://discord.com/developers/applications) and generate a bot token
* Rename `config.ini.example` to `config.ini` and fill out the empty fields

* Install dependencies
```bash
$ pip install -r requirements.txt
```

* Run the bot
```bash
$ python camila.py
```

## Available commands
```
Music:
  join         Join the room occupied by the person invoking the command.
  leave        Leave the current voice channel
  pause        Pause the current playing video
  play         Play music from a YouTube video
  skip         Skip the current playing video
  unpause      Unpause the currently paused video
Plan:
  changeplan   Change the lesson plan for given group. Must have plan image a...
  plan         Display the lesson plan for given group
Randoms:
  randommember Choose a random member of given Discord role
  randomrange  Choose a random integer between given lower and upper bounds
​No Category:
  help         Shows this message

Type !help command for more info on a command.
You can also type !help category for more info on a category.
```

## License

Copyright (c) 2020 by ***Kamil Marut***

`SuperCamila` is under the terms of the [MIT License](https://www.tldrlegal.com/l/mit), following all clarifications stated in the [license file](LICENSE).