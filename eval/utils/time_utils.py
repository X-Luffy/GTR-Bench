def convert_seconds_to_timecode(seconds: float,start_hours: float = 12) -> str:
    """将秒数转换为HH:MM:SS.sss格式"""
    hours, rem = divmod(seconds, 3600)
    mins, secs = divmod(rem, 60)
    hours += start_hours
    return f"{int(hours):02}:{int(mins):02}:{secs:06.3f}"

def format_time(time_tuple):
    """将时间元组(start, end)格式化为字符串（示例格式，可根据需要调整）"""
    start, end = time_tuple
    start = convert_seconds_to_timecode(start)
    end = convert_seconds_to_timecode(end)
    return f"{start}-{end}"

