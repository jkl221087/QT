from datetime import datetime

# 获取当前时间
current_time = datetime.now()

# 计算距离下一个整点的时间间隔
next_hour = current_time.replace(hour=current_time.hour + 1, minute=0, second=0, microsecond=0)
time_until_next_hour = next_hour - current_time

# 将时间间隔转换成秒数
seconds_until_next_hour = time_until_next_hour.total_seconds()

print("距离下一个整点还有", seconds_until_next_hour, "秒")
