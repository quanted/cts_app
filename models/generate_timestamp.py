from datetime import datetime
import pytz

def gen_jid(self):
	ts = datetime.now(pytz.UTC)
	localDatetime = ts.astimezone(pytz.timezone('US/Eastern'))
	jid = localDatetime.strftime('%Y%m%d%H%M%S%f')
	return jid