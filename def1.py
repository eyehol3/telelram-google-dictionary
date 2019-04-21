import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import logging
import json
import requests
# import sys

TOKEN = ''

bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					 level=logging.INFO)

dispatcher = updater.dispatcher
bot = telegram.Bot(token=TOKEN)


def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Hi. Try sending an english word to me")
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

url = ('https://googledictionaryapi.eu-gb.mybluemix.net')
lang = 'en'
###formatting
def it(a):
	return('_{}:_ '.format(a))
def bd(b):
	return('*{}* '.format(b))

def word(bot, update):
	try:
		word = update.message.text
		r = requests.get(('{}/?define={}&lang={}').format(url, word, lang))
		data = r.json()
		msg = ''
		count = 0
		for wrd in data:
			count +=1
			##checking presence of phonetic
			if 'phonetic' in wrd:
				msg += it(wrd['phonetic']) + '\n'
			else:
				msg += it(word) + '\n'
				##returning parts of speech
			for part, meanings in wrd['meaning'].items():
				number = 1
				msg += bd(part) + ' '
				for meaning in meanings:
					ind = meanings.index(meaning)
					##for each returning meaning(s)
					msg += str(number) + '. '
					for k, l in meanings[ind].items():

						if type(l) == list and len(meanings) == 1 and len(data) < 2:
							msg += it(k) + ', '.join(l) + '\n'
						elif type(l) == list and (len(data) > 1 or len(meanings) > 1):
							pass
						else:
							msg += it(k) + l + '\n'
					number += 1
				msg += '\n'
			msg += '\n'

		bot.send_message(chat_id=update.message.chat_id, text =(msg), parse_mode=telegram.ParseMode.MARKDOWN)
	except Exception as error:
		print('Caught this error: ' + repr(error))
		raise error.with_traceback(sys.exc_info()[2])
		bot.send_message(chat_id=update.message.chat_id, text =("I couldn't find this word. Your current language is {}.".format(bd(lang))), parse_mode=telegram.ParseMode.MARKDOWN)


word_handler = MessageHandler(filters.Filters.text, word)
dispatcher.add_handler(word_handler)

updater.start_polling()
updater.idle()
