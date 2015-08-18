import datetime

__author__ = 'Sapocaly'


# unicode to integer (unit: cent)
def unicode2int(unicode_str):
    return int(float(str(unicode_str)) * 100)


def int2float(int_num):
    pass


def db_time_format(string):
    yyyy = int(string[:4])
    MM = int(string[5:7])
    dd = int(string[8:10])
    hh = int(string[11:13])
    mm = int(string[14:16])
    ss = int(string[17:19])
    time = datetime.datetime(yyyy, MM, dd, hh, mm, ss)
    return time


def chop_microseconds(time):
    return time - datetime.timedelta(microseconds=time.microsecond)