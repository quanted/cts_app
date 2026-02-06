from datetime import datetime, timezone
from zoneinfo import ZoneInfo

def gen_jid(self):
	ts = datetime.now(timezone.utc)
	localDatetime = ts.astimezone(ZoneInfo('US/Eastern'))
	jid = localDatetime.strftime('%Y%m%d%H%M%S%f')
	return jid