import datetime

from PIL import Image
import numpy as np


def png_to_bmp(png_path, bmp_path):
    img = Image.open(png_path)
    ary = np.array(img)

    if len(ary.shape) == 3:
        ary = ary.mean(axis=2)

    # bitmap = np.dot((ary > 200).astype(float),255)
    im = Image.fromarray(ary.astype(np.uint8))
    im.save(bmp_path)
    return bmp_path


MINUTE_OFFSET = 1
UPDATE_HOURS = list(range(6, 23))


def calculate_update_time():
    """
    calculates the time to sleep and target datetime until the specified time of day
    :param target_hour:
    :param target_minute:
    :param target_second:
    :return:
    """
    now = datetime.datetime.now()

    # check the for the next update time
    later_values = list(filter(lambda x: x > now.hour, UPDATE_HOURS))
    target_hour = later_values[0] if len(later_values) > 0 else min(UPDATE_HOURS)

    target_time_today = now.replace(
        hour=target_hour, minute=MINUTE_OFFSET, second=0, microsecond=0
    )

    if target_time_today < now:
        # Target time has already passed today, so set it for tomorrow
        target_time = target_time_today + datetime.timedelta(days=1)
    else:
        # Target time has not yet passed today, so set it for today
        target_time = target_time_today

    time_to_sleep = int((target_time - now).total_seconds())
    return {"target_time": target_time, "time_to_sleep": time_to_sleep}
