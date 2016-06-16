import websocket
import _thread as thread
import time
import sys
import json
import os
import random
import items


def test(streamer, server):

	auth = {
		"event": "auth",
		"data": "8d49af56-fdd8-47ea-9a2c-d7711c81f229"
	}

	server = server
	print(server)

	# Path to Python.. can be python2.7 or above for this entry
	# PYTHON_PATH = '<PATH_TO_PYTHON>';

	# Path to Python Telnet Script - USE "/" as separator even on Windows
	pyscript_path = './telnet.py'

	# 7 Days to Die Player Name
	steam = server['username']

	sub = {
		"event": "subscribe",
		"data": "commands"
	}

	# Spawn Lists
	# items = [ITEM, QUANTITY]
	weapons = items.items['weapons']
	explosives = items.items['explosives']
	parts = items.items['parts']
	tools = items.items['tools']
	clothes = items.items['clothes']
	health = items.items['health']
	food = items.items['food']
	books = items.items['books']
	quests = items.items['quests']
	misc = items.items['misc']
	buffs = items.items['buffs']
	debuffs = items.items['debuffs']

	# Random range of numbers
	num = random.randrange(0, 100)
	amt = random.randrange(0, 20)

	###################################################################################
	# ##########################   NO EDIT BELOW THIS LINE   ######################## #
	###################################################################################

	def on_message(ws, message):
		response = json.loads(message)
		data = []

		# check if the key event is in the response dict
		if 'event' in response:
			# if there store the value
			event = response['event']
			# check if the value is cmdran
			if event == 'cmdran':
				# if if is cmdran append the values to the data dict
				data.append(response['data']['rawcommand'])
				data.append(response['data']['username'])
				data.append(response['data']['userid'])

				print(data)
				if data[0] == '!animal':
					key = random.randrange(0, len(friends))
					os.system('python {} {} {} {} 3 spawnentity {} {}'.format(pyscript_path, server['host'], server['port'], server['password'], steam, friends[key]))

				# Spawn Enemy
				elif data[0] == '!zombie':
					key = random.randrange(0, len(enemies))
					if num == 73:
						os.system('python {} {} {} {} 2 spawnwanderinghorde'.format(pyscript_path, server['host'], server['port'], server['password']))
					else:
						os.system('python {} {} {} {} 2 spawnentity {} {}'.format(pyscript_path, server['host'], server['port'], server['password'], steam, enemies[key]))

				# Spawn Item
				elif data[0] == '!item':
					key = random.randrange(0, len(items))
					if num == 73:
						os.system('python {} {} {} {} 1 spawnairdrop'.format(pyscript_path, server['host'], server['port'], server['password']))
					else:
						os.system('python {} {} {} {} 4 give {} {} {}'.format(pyscript_path, server['host'], server['port'], server['password'], steam, items[key][0], items[key][1]))

				# Spawn Horde
				elif data[0] == '!horde':
					os.system('python {} {} {} {} 2 spawnwanderinghorde'.format(pyscript_path, server['host'], server['port'], server['password']))

				# Spawn Feral
				elif data[0] == '!feral':
					os.system('python {} {} {} {} 2 spawnentity {} zombieFeral'.format(pyscript_path, server['host'], server['port'], server['password'], steam))

				elif data[0] == '!screamer':
					os.system('python {} {} {} {} 2 spawnentity {} zombieScreamer'.format(pyscript_path, server['host'], server['port'], server['password'], steam))

				# Spawn Airdrop
				elif data[0] == '!airdrop':
					os.system('python {} {} {} {} 1 spawnairdrop'.format(pyscript_path, server['host'], server['port'], server['password']))

	# if error is thrown
	def on_error(ws, error):
		print(error)

	# if connection is closed
	def on_close(ws):
		print("### closed ###")

	# open the connection
	def on_open(ws):
		def run(*args):

			# send the auth and sub data
			ws.send(json.dumps(auth))
			ws.send(json.dumps(sub))

			# keep sending to keep the connection open
			while True:
				time.sleep(10)
				ws.send(json.dumps(sub))

		thread.start_new_thread(run, ())

# if __name__ == "__main__":
	websocket.enableTrace(True)
	if len(sys.argv) < 2:
		host = "wss://api.scottybot.net/websocket/control"
	else:
		host = sys.argv[1]
	ws = websocket.WebSocketApp(host,
					on_message=on_message,
					on_error=on_error,
					on_close=on_close)
	ws.on_open = on_open

	ws.run_forever()
