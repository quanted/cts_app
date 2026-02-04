from datetime import datetime, timezone
from zoneinfo import ZoneInfo

def gen_jid(self):
	ts = datetime.now(timezone.UTC)
	localDatetime = ts.astimezone(ZoneInfo.timezone('US/Eastern'))
	jid = localDatetime.strftime('%Y%m%d%H%M%S%f')
	return jid