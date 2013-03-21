#!/usr/bin/env python
import os
import sys
import signal
from daemon import Daemon
from time import time, sleep
from os.path import expanduser
import shutil


HOME = expanduser("~")
PATH = HOME + '/.browser-man-switch/'
FILENAME = 'last_runtime'
CHROME_DATA_PATH = HOME + "/Library/Application Support/Google/Chrome/Default/"
CHROME_APPLICATION_PATH = "/Applications/Google Chrome.app/"
FIREFOX_DATA_PATH = HOME + ""
FIREFOX_APPLICATION_PATH = ""
SAFARI_DATA_PATH = HOME + ""
SAFARI_APPLICATION_PATH = ""


class HistoryDeleter(Daemon):

    def __init__(self, chrome=True, firefox=False, safari=False, length=7, pidfile=None):
        self._ensure_dir(PATH)
        super(HistoryDeleter, self).__init__(pidfile)
        self.chrome = chrome
        self.firefox = firefox
        self.safari = safari
        self.length = length

    #
    # Handle file opening / creating / reading / writing
    #

    def _ensure_dir(f):
        d = os.path.dirname(f)
        if not os.path.exists(d):
            os.makedirs(d)

    def _touch(fname, times=None):
        with file(fname, 'a'):
            os.utime(fname, times)

    #
    # Get last access time of browsers
    #

    def _get_last_access_time(self, path):
        return os.stat(path).st_atime

    def get_last_access_time(self):
        access_time = 0
        if self.chrome:
            access_time = max(access_time, self._get_last_access_time(CHROME_APPLICATION_PATH))
        if self.firefox:
            access_time = max(access_time, self._get_last_access_time(FIREFOX_APPLICATION_PATH))
        if self.safari:
            access_time = max(access_time, self._get_last_access_time(SAFARI_APPLICATION_PATH))

        return access_time

    #
    # Main logic functions
    #

    def _seconds_to_hours(self, seconds):
        return seconds * 1/60 * 1/60

    def _used_recently(self):
        '''
        Return True if a browser was recently used,
        otherwise return false
        '''
        last_access_time = self.get_last_access_time()
        seconds_ago = time() - last_access_time

        hours_ago = self._seconds_to_hours(seconds_ago)

        if hours_ago > self.length:
            return False

        return True

    def do_cleanup(self):
        print "do cleanup"
        if self._used_recently():
            return

        # Nuke this shit
        if self.chrome:
            try:
                shutil.rmtree(CHROME_DATA_PATH)
            except Exception, e:
                print "fail"
                print e

        if self.firefox:
            pass

        if self.safari:
            pass

    def run_loop(self):
        '''
        Check if we need to attempt cleanup
        '''
        while True:
            if self.check_needs_cleanup():
                self.do_cleanup()

            sleep(60)

    def run(self):
        self.run_loop()


def signal_handler(signum, frame):
    '''
    This implicitly kills all child threads as well.
    '''

    print "\nCaught Ctrl-C... exiting"
    sys.exit(0)


if __name__ == "__main__":
    try:
        import argparse

        signal.signal(signal.SIGINT, signal_handler)
        parser = argparse.ArgumentParser(description='Delete your browser history after you die. OSX Only')
        parser.add_argument('-c', '--chrome', action='store_true', dest="CHROME",
                            help='delete history from chrome')
        parser.add_argument('-f', '--firefox', action='store_true', dest="FIREFOX",
                            help='delete history from firefox')
        parser.add_argument('-s', '--safari', action='store_true', dest="SAFARI",
                            help='delete history from safari')
        parser.add_argument('-t', '--time', type=float, dest="TIME",
                            help='how many days of no browser usage until we assume you are dead?')
        parser.add_argument('-d', '--daemon', type='store_true', dest="DAEMON",
                            help='should this run as a background daemon?')

        args = parser.parse_args()

        # if args.PORT:
        #     PORT = args.PORT
        # if args.PATH:
        #     FILE_PREFIX = args.PATH
        if args.TIME:
            length = args.TIME
        else:
            length = 7

        daemon = HistoryDeleter(chrome=args.CHROME or (not args.FIREFOX and not args.SAFARI), firefox=args.FIREFOX, safari=args.SAFARI, length=length, pidfile=PATH + '.switch.pid')

        if args.DAEMON:
            daemon.start()
        else:
            daemon.run()

    except Exception:
        # Could not successfully import argparse or something
        pass
