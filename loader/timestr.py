def timestr(seconds):
    a = str(int(seconds//3600))
    b = str(int((seconds%3600)//60))
    c = str(round((seconds%3600)%60,2))
    time = f"{a}h {b}m {c}s"
    return time