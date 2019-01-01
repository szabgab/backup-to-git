#!/usr/bin/env python

import os
import subprocess
import shutil

'''
TODO:
For now pathes are mostly hard coded. Allow more flexible configurations.
Handle also the removal of files and directories.
Logging
Error handling
Test the various cases.
'''

def backup():
    git_dir = os.path.dirname(os.path.abspath(__file__))
    dropbox_dir = '/home/gabor/Dropbox/notes'
    
    git = 'git'
    
    if not os.path.exists(dropbox_dir):
        exit('Dropbox direcory "{dropbox_dir}" does not exist'.format(dropbox_dir = dropbox_dir))

    for thing in os.listdir(dropbox_dir):
        path_to = os.path.join(dropbox_dir, thing)
        if os.path.isfile(path_to):
            shutil.copy(path_to, git_dir)
        elif os.path.isdir(path_to):
            shutil.copytree(path_to, git_dir)
        else:
            print('Not file and not directory {}'.format(thing))
    os.chdir(git_dir)
    status = subprocess.check_output([git, 'status', '--porcelain'])
    #print(status)
    if status:
        add = subprocess.check_output([git, 'add', '.'])
        commit = subprocess.check_output([git, 'commit', '-m', 'update'])
        push = subprocess.check_output([git, 'push'])

if __name__ == '__main__':
    backup()
