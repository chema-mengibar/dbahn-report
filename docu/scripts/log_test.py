import os
from os import listdir
from os.path import isfile, join
import logging

CURRENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),"./"))

#logging.debug(datetime.now().strftime("%d_%m_%Y") + " inicio rutina")
#logger = logging.getLogger(__name__)
#logger.info('Start reading database')
#logging.basicConfig(filename=  str(station["evaNumber"]) + '.log',level=logging.DEBUG)
#logger.debug(  "saving: station-" + str(station["evaNumber"]) + " day-" +   l_day )
#logger.debug(  "saved: station-" + str(station["evaNumber"]) + " day-" +   l_day )

filename= CURRENT_DIR +'/data/logTest' + str('001') + '.log'

log = logging.getLogger()
log.setLevel(logging.INFO)
fh = logging.FileHandler(filename= filename)
fh.setLevel(logging.INFO)
formatter = logging.Formatter(
            fmt='%(asctime)s %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
            )
fh.setFormatter(formatter)
log.addHandler(fh)

log.info('-------Start--------')
log.info('this function is doing something')
log.info('this function is finished')
log.removeHandler(fh)
del log,fh



filename= CURRENT_DIR +'/data/logTest' + str('002') + '.log'

log = logging.getLogger()
log.setLevel(logging.INFO)
fh = logging.FileHandler(filename= filename)
fh.setLevel(logging.INFO)
formatter = logging.Formatter(
            fmt='%(asctime)s %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
            )
fh.setFormatter(formatter)
log.addHandler(fh)

log.info('-------Start--------')
log.info('this function is doing something 2')
log.info('this function is finished 2')
log.removeHandler(fh)
del log,fh
