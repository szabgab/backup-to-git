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
'''

class Backup(object):
    def main(self):
        logging.basicConfig(level = logging.INFO)
        args, config = self.get_config()

        self.copy_files(config)

        if args.git:
            self.commit_to_git(config)

    def commit_to_git(self, config):
        target_dir = config['target']
        git = 'git'

        os.chdir(target_dir)
        status = subprocess.check_output([git, 'status', '--porcelain'])
        print(status)
        if status:
            print("Commit files")
            add = subprocess.check_output([git, 'add', '.'])
            commit = subprocess.check_output([git, 'commit', '-m', 'update'])
            push = subprocess.check_output([git, 'push'])


    def copy_files(self, config):
        target_dir = config['target']
        if not os.path.exists(target_dir):
            exit('Target directory "{target_dir}" does not exist'.format(target_dir = target_dir))
        os.chdir(target_dir)

        if 'source' in config:
            source_dir = config['source']
            self.backup_full_dir(source_dir, target_dir)
        elif 'pairs' in config:
            for pair in config['pairs']:
                if os.path.exists(pair['src']):
                    target_path = os.path.join(target_dir, pair['trg'])
                    if not os.path.exists(target_path):
                        os.mkdir(target_path)
                    self.backup_full_dir(pair['src'], target_path)
                else:
                    raise Exception('Invalid configuration file - src')
        else:
            raise Exception('Invalid configuration file')

    def get_config(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--config', help='Config file', required=True)
        parser.add_argument('--git',    help='Run the git commands', action='store_true')
        args = parser.parse_args()

        if not os.path.exists(args.config):
            exit('"{}" does not exist'.format(args.config))

        with open(args.config) as fh:
            config = json.load(fh)
        #print(config)
        return args, config


    def backup_full_dir(self, source_dir, target_dir):
        if not os.path.exists(source_dir):
            exit('Source directory "{source_dir}" does not exist'.format(source_dir = source_dir))

        for dirName, subdirList, fileList in os.walk(source_dir):
            dir_part = dirName[len(source_dir)+1:]

            for dr in subdirList:
                trg = os.path.join(target_dir, dir_part, dr)
                logging.info('Make dir {}'.format(trg))
                if not os.path.exists(trg):
                    os.mkdir(trg)

            for fname in fileList:
                src = os.path.join(dirName, fname)
                trg = os.path.join(target_dir, dir_part, fname)
                #logging.info('Copy file {} to {}'.format(src, trg))
                shutil.copy(src, trg)

        for dirName, subdirList, fileList in os.walk(target_dir):
            if '.git' in subdirList:
                subdirList.remove('.git')
            dir_part = dirName[len(target_dir)+1:]
            #print("DIR: " + dir_part)
            for dr in subdirList:
                trg = os.path.join(target_dir, dir_part, dr)
                src = os.path.join(source_dir, dir_part, dr)
                if not os.path.exists(src):
                    logging.info('Remove {}'.format(trg))
                    shutil.rmtree(trg)

            for fname in fileList:
                src = os.path.join(source_dir, dir_part, fname)
                trg = os.path.join(dirName, fname)
                #print("SRC: " + src)
                #print("TRG: " + trg)
                if not os.path.exists(src):
                    logging.info('Remove {}'.format(trg))
                    os.remove(trg)



if __name__ == '__main__':
    Backup().main()
