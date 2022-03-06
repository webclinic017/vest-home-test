from datetime import date
import logging

logging.basicConfig(
    level="ERROR",
    format='%(asctime)s %(levelname)-8s %(name)-12s %(message)s',
    datefmt='%d-%m-%Y %H:%M',
    filename='./log/log_{}.log'.format(date.today().strftime('%d-%m-%Y'))
)

log = logging.getLogger()