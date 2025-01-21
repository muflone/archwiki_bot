#!/usr/bin/env python
##
#     Project: ArchWiki_bot
# Description: Telegram bot to search pages on the Arch Linux Wiki
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2025 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

import logging
import os
import uuid

import requests

import telegram
import telegram.ext

WIKI_URL = 'https://wiki.archlinux.org'


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
# Set higher logging level for httpx to avoid all GET and POST requests
# being logged
logging.getLogger('httpx').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

caching = {}


async def command_start(update: telegram.Update,
                        context: telegram.ext.ContextTypes.DEFAULT_TYPE
                        ) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hi, use /help!')


async def command_help(update: telegram.Update,
                       context: telegram.ext.ContextTypes.DEFAULT_TYPE
                       ) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(f'Use {context.bot.name} Search term')


async def inline_query(update: telegram.Update,
                       context: telegram.ext.ContextTypes.DEFAULT_TYPE
                       ) -> None:
    """Handle the inline query."""
    query = update.inline_query.query
    if not query:
        # empty query should not be handled
        return

    if query in caching:
        data = caching[query]
        logging.info(f'Get from cache: {query}')
    else:
        api_url = f'{WIKI_URL}/rest.php/v1/search/title?q={query}&limit=10'
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            caching[query] = data
            logger.info(query)
        except requests.RequestException as error:
            logger.error(f'Error fetching data from Arch Wiki: {error}')

    # Process the search results
    results = []
    for page in data.get('pages', []):
        title = page['title']
        page_url = f'{WIKI_URL}/title/{title.replace(' ', '_')}'

        results.append(telegram.InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title=title,
            input_message_content=telegram.InputTextMessageContent(page_url),
            description=page_url))

    # Answer the inline query with the results
    await update.inline_query.answer(results, cache_time=60)


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = telegram.ext.Application.builder().token(
        token=os.environ.get('TELEGRAM_TOKEN')).build()

    # on different commands - answer in Telegram
    application.add_handler(handler=telegram.ext.CommandHandler(
        command='start',
        callback=command_start))
    application.add_handler(handler=telegram.ext.CommandHandler(
        command='help',
        callback=command_help))

    # on inline queries - show corresponding inline results
    application.add_handler(handler=telegram.ext.InlineQueryHandler(
        callback=inline_query))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=telegram.Update.ALL_TYPES)


if __name__ == '__main__':
    main()
