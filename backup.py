#!/usr/bin/env python

import argparse
import logging
import json
import os
import shutil
import subprocess

'''
TODO:
For now pathes are mostly hard coded. Allow more flexible configurations.
Handle also the removal of files and directories.
Logging
Error handling
Test the various cases.
'''

def run():
    if not os.path.exists(args.config):
        exit('"{}" does not exist'.format(args.config)) 

    with open(args.config) as fh:
        config = json.load(fh)
    #print(config)

    target_dir = config['target']
    source_dir = config['source']
    
    git = 'git'
    
    if not os.path.exists(source_dir):
        exit('Source directory "{source_dir}" does not exist'.format(source_dir = source_dir))

    for thing in os.listdir(source_dir):
        logging.info(thing)
        path_to = os.path.join(source_dir, thing)
        if os.path.isfile(path_to):
            logging.info('Copy file {} to {}'.format(path_to, target_dir))
            shutil.copy(path_to, target_dir)
        elif os.path.isdir(path_to):
            logging.info('Copy tree {} to {}'.format(path_to, target_dir))
            shutil.copytree(path_to, target_dir)
        else:
            print('Not file and not directory {}'.format(thing))
    os.chdir(target_dir)
    status = subprocess.check_output([git, 'status', '--porcelain'])
    #print(status)
    #if status:
    #    add = subprocess.check_output([git, 'add', '.'])
    #    commit = subprocess.check_output([git, 'commit', '-m', 'update'])
    #    push = subprocess.check_output([git, 'push'])

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='Config file', required=True)
    args = parser.parse_args()
    run()
