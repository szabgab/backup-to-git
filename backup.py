#!/usr/bin/env python

import argparse
import logging
import json
import os
import shutil
import subprocess

'''
TODO:
Allow more flexible configurations.
Handle also the removal of files and directories.
Logging
Error handling
Test the various cases.
'''

class Backup(object):
    def copy_file(self, src, trg):
        logging.info('Copy file {} to {}'.format(src, trg))
        shutil.copy(src, trg)
    def make_dir(self, trg):
        logging.info('Make dir {}'.format(trg))
        if not os.path.exists(trg):
            os.mkdir(trg)

    def main(self):
        logging.basicConfig(level = logging.INFO)

        parser = argparse.ArgumentParser()
        parser.add_argument('--config', help='Config file', required=True)
        parser.add_argument('--git',    help='Run the git commands', action='store_true')
        args = parser.parse_args()

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

        for dirName, subdirList, fileList in os.walk(source_dir):
            for dr in subdirList:
                self.make_dir( os.path.join(target_dir, dr) )
            dir_part = dirName[len(source_dir)+1:]
            for fname in fileList:
                self.copy_file(os.path.join(dirName, fname), os.path.join(target_dir, dir_part, fname))


        os.chdir(target_dir)
        if args.git:
            status = subprocess.check_output([git, 'status', '--porcelain'])
            print(status)
            if status:
                add = subprocess.check_output([git, 'add', '.'])
                commit = subprocess.check_output([git, 'commit', '-m', 'update'])
                push = subprocess.check_output([git, 'push'])

if __name__ == '__main__':
    Backup().main()
