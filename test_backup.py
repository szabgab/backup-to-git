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

    def make_dir(self, trg):
       self.events.append(['make_dir', trg])

def test_backup(tmpdir):
    tmp_dir = str(tmpdir)  # Needed for Python 3.5 and older
    print(tmp_dir)
    source_dir = os.path.join(tmp_dir, 'src')
    target_dir = os.path.join(tmp_dir, 'target')
    config_file = os.path.join(tmp_dir, 'cfg.json')
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


    os.mkdir(os.path.join(source_dir, 'songs'))
    with open(os.path.join(source_dir, 'songs', 'yesterday.txt'), 'w') as fh:
       fh.write('Beatles')

    bck = TBackup()
    bck.main()
    print(bck.events)
    assert bck.events == [
        ['make_dir',  os.path.join(target_dir, 'songs')],
        ['copy_file', os.path.join(source_dir, 'a.txt'), os.path.join(target_dir, 'a.txt')],
        ['copy_file', os.path.join(source_dir, 'songs', 'yesterday.txt'), os.path.join(target_dir, 'songs', 'yesterday.txt')],
    ]


    os.mkdir(os.path.join(source_dir, 'songs', 'spanish'))
    with open(os.path.join(source_dir, 'songs', 'spanish', 'despacio.txt'), 'w') as fh:
       fh.write('Slowly!')

    bck = TBackup()
    bck.main()
    print(bck.events)
    assert bck.events == [
        ['make_dir',  os.path.join(target_dir, 'songs')],
        ['copy_file', os.path.join(source_dir, 'a.txt'), os.path.join(target_dir, 'a.txt')],
        ['make_dir',  os.path.join(target_dir, 'songs', 'spanish')],
        ['copy_file', os.path.join(source_dir, 'songs', 'yesterday.txt'), os.path.join(target_dir, 'songs', 'yesterday.txt')],
        ['copy_file', os.path.join(source_dir, 'songs', 'spanish', 'despacio.txt'), os.path.join(target_dir, 'songs', 'spanish', 'despacio.txt')],
    ]


