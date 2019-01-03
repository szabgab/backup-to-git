import json
import os
import sys

import backup

# create a temporary directory for the source files
# create a temp directory for the git repository
# run the backup
# check the results
#backup.run()

class TBackup(backup.Backup):
    def __init__(self):
       self.events = []

    def copy_file(self, src, trg):
       self.events.append(['copy_file', src, trg])

def test_backup(tmpdir):
    print(tmpdir)
    source_dir = os.path.join(tmpdir, 'src')
    target_dir = os.path.join(tmpdir, 'target')
    config_file = os.path.join(tmpdir, 'cfg.json')
    os.mkdir(source_dir)
    os.mkdir(target_dir)

    with open(config_file, 'w') as fh:
       json.dump({
	   'source': source_dir,
	   'target': target_dir,
       }, fh)

    print(sys.argv)
    sys.argv = ['backup', '--config', config_file]
    bck = TBackup()
    bck.main()
    assert bck.events == []

    with open(os.path.join(source_dir, 'a.txt'), 'w') as fh:
       fh.write('hello')


    bck = TBackup()
    bck.main()
    assert bck.events == [
        ['copy_file', os.path.join(source_dir, 'a.txt'), os.path.join(target_dir, 'a.txt')],
    ]
