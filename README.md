<p align="center">
  <a href="https://github.com/SergeyIvanovDevelop/VK-Bot">
    <img alt="VK-Bot" src="./resources/VK-Bot.png"/>
  </a>
</p>
<h1 align="center">
  VK-Bot
</h1>

## VK-Bot &middot; [![GitHub license](https://img.shields.io/badge/license-CC%20BY--NC--SA%203.0-blue)](./LICENSE) [![Python](https://img.shields.io/badge/language-python-orange)](https://www.python.org/) [![VK](https://img.shields.io/badge/social%20network-VK-blue)](https://vk.com/) [![LinkedIn](https://img.shields.io/badge/linkedin-Sergey%20Ivanov-blue)](https://www.linkedin.com/in/sergey-ivanov-33413823a/) [![Telegram](https://img.shields.io/badge/telegram-%40SergeyIvanov__dev-blueviolet)](https://t.me/SergeyIvanov_dev) ##

This repository contains the bot implementation code for the [VK](https://vk.com/) social network, assigned to a specific group in `VK` (photographer's group). The bot allows you to find out information about the photographer, the cost of a photo shoot, send a request to the photographer to book a photo shoot, also see examples of work and send messages to those users who are already in correspondence with the bot.

## :computer: Getting Started  ##

**Step 1**

1. Go to home directory and clone repository from github: `cd ~ && git clone https://SergeyIvanovDevelop@github.com/SergeyIvanovDevelop/VK-Bot`

**Step 2**<br>

2. Go to the directory of the downloaded repository: `cd ~/VK-Bot`

**Step 3**<br>

3. Installing dependencies:

```
pip3 install -r ./requirements.txt
```

**Step 4**<br>

_Note: before starting in the `vk_bot.py` script, you must enter your authorization data, data for the group, etc. How to get them - refer to the `VK` manual, valid at the time of reading this `README.md`. Also, to customize your bot, change the thematic information located in [vk_bot.py](./vk_bot.py) and [keyboard.json](./keyboard.json)_

4. Run application: `python3 vk_bot.py`


**:clapper: Example using (GIF):**<br>

This animation demonstrates scenarios for using the VK-Bot.<br>

<p align="center">
  <img src="./resources/VK-Bot.gif" alt="animated" />
</p>

### :bookmark_tabs: Licence ###
VK-Bot is [CC BY-NC-SA 3.0 licensed](./LICENSE).
