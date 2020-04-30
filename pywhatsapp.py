#!/usr/bin/env python

###########################################################################
#   Author: Roman Fainerman                                               #
#   28/04/2020                                                            #
#   Description: Send whatsapp message from sonarr/radarr                 #
###########################################################################

import os
from twilio.rest import Client
from python_logger import getargs, log
import re

args = getargs().args_start(
    "This script is used to send whatsapp messages to myself about sonarr and radarr downloads")
logger = log(args).start_logger(args)


def check_event():
    if os.getenv('radarr_isupgrade') == 'True' or os.getenv('sonarr_isupgrade') == 'True':
        event = 'Upgrade'
    elif os.getenv('radarr_isupgrade') == 'False' or os.getenv('sonarr_isupgrade') == 'False':
        event = 'Download'
    else:
        logger.error(logger.info('Couldn\'t figure out if upgrade or download'))
        exit(100)

    return event


def get_event(agent, event, msg):
    MESSAGE = (msg)
    logger.info(
        'got an event from {} - {}'.format(agent, event))
    return MESSAGE


def main():
    event = check_event()
    if os.getenv('sonarr_eventtype') is not None:
        MESSAGE = get_event('sonarr', event, '{}ed show {} Season {} Episode {}, quality level is {} to {}'.format(event, os.getenv('sonarr_series_title'), os.getenv(
            'sonarr_episodefile_seasonnumber'), os.getenv('sonarr_episodefile_episodenumbers'), os.getenv('sonarr_episodefile_quality'), os.getenv('sonarr_series_path'))).replace('Upgradeed', 'Upgraded')
    elif os.getenv('radarr_eventtype') is not None:
        MESSAGE = get_event('radarr', event, '{}ed movie {}, quality level is {} to {}'.format(event, os.getenv(
            'radarr_movie_title'), os.getenv('radarr_moviefile_quality'), os.getenv('radarr_movie_path'))).replace('Upgradeed', 'Upgraded')
    else:
        logger.error('Couldn\'t get event type')
        exit(100)

    client = Client()
    # this is the Twilio sandbox testing number
    from_whatsapp_number = 'whatsapp:+<replace_this>'
    # replace this number with your own WhatsApp Messaging number
    to_whatsapp_number = 'whatsapp:+<replace_this>'

    try:
        client.messages.create(body=MESSAGE,
                               from_=from_whatsapp_number,
                               to=to_whatsapp_number)
        logger.info("Whatsapp message \"{}\" was succesfully sent to {}".format(
            MESSAGE, re.split(":", to_whatsapp_number)[1]))
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    main()
