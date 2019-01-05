import json
import os
import sys

from backup import Backup

# create a temporary directory for the source files
# create a temp directory for the git repository
# run the backup
# check the results: check if the correct files exist in the target area after a run.

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

   # pretend the git repository
    os.mkdir(os.path.join(target_dir, '.git'))
    with open(os.path.join(target_dir, '.git', 'HEAD'), 'w') as fh:
       fh.write('head')


    print(sys.argv)
    sys.argv = ['backup', '--config', config_file]
    bck = Backup()
    bck.main()
    assert os.listdir(target_dir) == ['.git']


    with open(os.path.join(source_dir, 'a.txt'), 'w') as fh:
       fh.write('hello')

    bck = Backup()
    bck.main()
    assert os.listdir(target_dir) == ['.git', 'a.txt']


    os.mkdir(os.path.join(source_dir, 'songs'))
    with open(os.path.join(source_dir, 'songs', 'yesterday.txt'), 'w') as fh:
       fh.write('Beatles')

    bck = Backup()
    bck.main()
    assert os.listdir(target_dir) == ['.git', 'songs', 'a.txt']
    assert os.listdir(os.path.join(target_dir, 'songs')) == ['yesterday.txt']


    os.mkdir(os.path.join(source_dir, 'songs', 'spanish'))
    with open(os.path.join(source_dir, 'songs', 'spanish', 'despacio.txt'), 'w') as fh:
       fh.write('Slowly!')
    with open(os.path.join(source_dir, 'songs', 'spanish', 'rapido.txt'), 'w') as fh:
       fh.write('Fast!')

    bck = Backup()
    bck.main()
    assert os.listdir(target_dir) == ['.git', 'songs', 'a.txt']
    assert os.listdir(os.path.join(target_dir, 'songs')) == ['yesterday.txt', 'spanish']
    assert os.listdir(os.path.join(target_dir, 'songs', 'spanish')) == ['despacio.txt', 'rapido.txt']

    assert os.path.exists(os.path.join(target_dir, '.git', 'HEAD'))


