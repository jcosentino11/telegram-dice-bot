from telegram.ext import Updater
from telegram.ext import CommandHandler
import sys
import logging
import random

# Reference: https://github.com/python-telegram-bot/python-telegram-bot   

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

ROLE_NUM_DICE = 0
ROLE_DICE_SIZE = 1
ROLE_MESSAGE = 2

def roll(bot, update):
	roll = parse_roll(update.message.text)
	result = execute_roll(roll)
	notify_user(bot, update, result, roll[ROLE_MESSAGE])

def parse_roll(command):
	text = command[3:] # trim '/r '

	d_index = index(text, 'd')
	space_index = index(text, ' ')
	
	# TODO better validation
	if d_index == -1:
		return None

	num_dice = text[:d_index]
	dice_size = text[d_index + 1: space_index if space_index != -1 else len(text)]
	message = "" if space_index == -1 else text[space_index + 1:]

	return (num_dice, dice_size, message)

def index(s, substring):
	try:
		return s.index(substring)
	except ValueError:
		return -1

def execute_roll(roll):
	num_dice = int(roll[ROLE_NUM_DICE])
	dice_size = int(roll[ROLE_DICE_SIZE])

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
	user = update.message.from_user.name
	text = '{0} rolled {1}.  {2}'.format(user, result, extra_msg)
	bot.send_message(chat_id=update.message.chat_id, text=text)

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