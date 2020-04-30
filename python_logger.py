#!/usr/bin/env python
"""
This is a generic class for logging
@Author: Roman Fainerman, System Linux Administrator
@Email: hubinhoo@gmail.com

"""
### IMPORTS ###
import argparse
import time
import sys
import logging
import os

class getargs(object):
    """
    This is to get arguments and store them

    """
    def args_start(self, desc):
        """
        this is initial function for args
        
        :return: args
        """
        parser = argparse.ArgumentParser(description=desc)
        parser.add_argument('-v', '--verbose', required=False, help='Enable verbose output', dest='verbose', action='store_true')
        parser.add_argument('-d', '--debug', required=False, help='Enable debug output', dest='debug', action='store_true')
        parser.add_argument('-l', '--log-file', required=False, help='file to log', dest='logfile')
        args = parser.parse_args()
        return args
        

class log:
    """
    This is a basic class for logging
        
    """
    def __init__(self, args):
        """
        This class will return the logger

        :return: logger
        """
        global log_level
        global log_file
        self.verbose = args.verbose
        self.debug = args.debug
        if args.logfile:
            log_file = args.logfile
        else:
            log_file = None
        ####Logging settings###
        if self.debug:
            log_level = logging.DEBUG
        elif self.verbose:
            log_level = logging.INFO
        else:
            log_level = logging.WARNING
        logging.basicConfig(filename=log_file, filemode='a',
                           format='%(asctime)s  %(levelname)s %(message)s', level=log_level, datefmt="%Y-%m-%d %H:%M:%S")
    def start_logger(self, args):
        self.logger = logging.getLogger(__name__)
        if log_file:
            out_hdlr = logging.StreamHandler(sys.stdout)
            out_hdlr.setFormatter(logging.Formatter('%(asctime)s  %(levelname)s %(message)s', datefmt="%Y-%m-%d %H:%M:%S"))
            self.logger.addHandler(out_hdlr)
        
        self.logger.debug('logger initialized ' + '--->' + " " + str(args).split("Namespace")[1] + '\n')
        return self.logger