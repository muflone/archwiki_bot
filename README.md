# ArchWiki_bot

**Description:** Telegram bot to search pages on the Arch Linux Wiki

**Copyright:** 2025 Fabio Castelli (Muflone) <muflone@muflone.com>

**License:** GPL-3+

**Source code:** https://github.com/muflone/archwiki_bot/

**Documentation:** http://www.muflone.com/archwiki_bot/

# Description

Search pages on the Arch Linux wiki by using @archwiki_bot followed
by the search term. For example:

```
@archwiki_bot Intel
```

Will present all the links associated to the Intel keyword.

# System Requirements

* Python >= 3.7 (developed and tested for Python 3.13)
* Python Telegram Bot ( https://pypi.org/project/python-telegram-bot/ )
* Requests ( https://pypi.org/project/requests/ )

# Usage

    cd /path/to/folder
    export TELEGRAM_TOKEN="YOUR:TOKEN"
    python3 main.py
