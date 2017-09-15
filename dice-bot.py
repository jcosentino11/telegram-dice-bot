from telegram.ext import Updater
from telegram.ext import CommandHandler
import sys
import logging
import random

# Reference: https://github.com/python-telegram-bot/python-telegram-bot   

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def roll(bot, update):
	roll = parse_roll(update.message.text)
	result = execute_roll(roll)
	notify_user(bot, update, result, roll[2])

def parse_roll(text):
	roll = text[3:] # trim '/r ''

	d_index = index(roll, 'd')
	space_index = index(roll, ' ')
	
	# TODO better validation
	if d_index == -1:
		return None

	return (roll[:d_index], roll[d_index + 1:], "" if space_index == -1 else roll[space_index + 1])

def index(s, substring):
	try:
		return s.index(substring)
	except ValueError:
		return -1

def execute_roll(roll):
	num_dice = int(roll[0])
	dice_size = int(roll[1])

	logger.info('num dice: {0}, dice_size: {1}'.format(num_dice, dice_size))

	total = 0
	message = ''

	for i in range(0, num_dice):
		result = random.randint(1, dice_size)
		if i == 0:
			message += '{0}'.format(result)
		else:
			message += ' + {0}'.format(result)
			
		total += result

	if message == '' or num_dice == 1:
		message = '{0}'.format(total)
	else:
		message += ' = {0}'.format(total)

	return message

def notify_user(bot, update, result, extra_msg=''):
	text = 'Yo fam rolled {0}. {1}'.format(result, extra_msg)
	bot.send_message(chat_id=update.message.chat_id, text=text)

def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def error(bot, update, error):
	logger.warn('Update "{0}" caused error "{1}"'.format(update, error))

def main():
	api_token = sys.argv[1]
	updater = Updater(api_token)

	dp = updater.dispatcher

	roll_handler = CommandHandler('r', roll)
	
	# handle roll commands
	dp.add_handler(roll_handler)

	# handle errors
	dp.add_error_handler(error)
	
	# Start the bot
	updater.start_polling()

	# Block until the program is interrupted
	updater.idle()

if __name__ == '__main__':
	main()