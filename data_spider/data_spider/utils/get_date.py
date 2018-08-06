"""generate List"""
from datetime import datetime, timedelta

def gen_dates(b_date, days):
    """
    generate date
    :param b_date: date
    :param days: days
    :return:
    """
    day = timedelta(days=1)
    for i in range(days):
        yield b_date + day*i

def get_date_list(start=None, end=None,start_str="2013-01-01"):
    """
    get date list
    :param start: start date
    :param end: end date
    :return:
    """
    if start is None:
        start = datetime.strptime(start_str, "%Y-%m-%d")
    if end is None:
        end = datetime.now()
    data = []
    for date_time in gen_dates(start, (end-start).days):
        data.append(date_time)
    return data

if __name__ == "__main__":
    for date in get_date_list():
        print(str(date).split()[0])
