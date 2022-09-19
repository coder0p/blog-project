import timeago
import datetime


def fromnow(date):
    return timeago.format(date, datetime.datetime.now())