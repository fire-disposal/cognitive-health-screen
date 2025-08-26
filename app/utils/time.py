import datetime
from datetime import datetime, timezone

get_current_time = lambda: datetime.now(tz=timezone.utc)