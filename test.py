from datetime import datetime
from zoneinfo import ZoneInfo

print(datetime.now(ZoneInfo("America/New_York")))
# 2022-03-29 11:20:30.917144-04:00