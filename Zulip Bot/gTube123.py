
# Zulip Bot by Team Ganador
import datetime
import os
import zulip
proxy = 'http://edcguest:edcguest@172.31.100.14:3128'
os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy

class gTube123(object):
	def usage(self):
		return "I am a Fun Bot !!! .... try me.."
	def handle_message(self, message, bot_handler):
		#currentDT = datetime.datetime.now()
		#print (str(currentDT))
		client = zulip.Client(config_file="/home/aayushshivam7/.local/lib/python3.5/site-packages/zulip_bots/bots/gTube123/zuliprc")
		request = {
			"type": "private",
			"to": "GTube1234-bot@hack36.zulipchat.com",
			"content": "yoyo"
		}
		result = client.send_message(request)
		if message['content'] == 'search':
			print('Searching your video')
handler_class = gTube123



