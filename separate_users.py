#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import gzip
import sys

def extract(user):
    """Returns the id, name from the json data"""
    #user = user.decode("iso-8859-1")
    j_form = json.loads(user.decode('UTF-8'))
    twitter_id, screen_name, location = j_form['id'], j_form['screen_name'], j_form['location']
    return twitter_id, screen_name, location


def extract_users_from_files(data_filename, save_filename):
    """Read the userinfo and leaves a (id, screen_name) summary"""
    with open(data_filename, 'r') as source_data:
        user_data = map(extract, source_data.readlines())

    with open(save_filename, 'w') as save_file:
        for user_id, user_name, location in user_data:
            save_file.write( '{0}\t{1}\t{2}\n'.format(user_id, location, user_name) )


if __name__ == '__main__':
	if len(sys.argv) < 2:
		raise Exception('Give me a file name to parse!')
	extract_users_from_files(sys.argv[1], sys.argv[1] + '.cleaned')

