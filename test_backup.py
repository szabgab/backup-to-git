import json
import os
import shutil
import sys

from backup import Backup

# create a temporary directory for the source files
# create a temp directory for the git repository
# run the backup
# check the results: check if the correct files exist in the target area after a run.

def test_one_dir_backup(tmpdir):
    tmp_dir = os.path.join(str(tmpdir), '1')  # Needed for Python 3.5 and older
    os.mkdir(tmp_dir)
    print('dir {}'.format(tmp_dir))
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


    #print(sys.argv)
    sys.argv = ['backup', '--config', config_file]
    bck = Backup()
    bck.main()
    assert os.listdir(target_dir) == ['.git']


    with open(os.path.join(source_dir, 'a.txt'), 'w') as fh:
       fh.write('hello')

    bck = Backup()
    bck.main()
    assert set(os.listdir(target_dir)) == set(['.git', 'a.txt'])


    os.mkdir(os.path.join(source_dir, 'songs'))
    with open(os.path.join(source_dir, 'songs', 'yesterday.txt'), 'w') as fh:
       fh.write('Beatles')

    bck = Backup()
    bck.main()
    assert set(os.listdir(target_dir)) == set(['.git', 'songs', 'a.txt'])
    assert os.listdir(os.path.join(target_dir, 'songs')) == ['yesterday.txt']


    os.mkdir(os.path.join(source_dir, 'songs', 'spanish'))
    with open(os.path.join(source_dir, 'songs', 'spanish', 'despacio.txt'), 'w') as fh:
       fh.write('Slowly!')
    with open(os.path.join(source_dir, 'songs', 'spanish', 'rapido.txt'), 'w') as fh:
       fh.write('Fast!')
    os.mkdir(os.path.join(source_dir, 'songs', 'hungarian'))
    with open(os.path.join(source_dir, 'songs', 'hungarian', 'macska-az-uton.txt'), 'w') as fh:
       fh.write('Tul van a dolgon')

    bck = Backup()
    bck.main()
    assert set(os.listdir(target_dir)) == set(['.git', 'songs', 'a.txt'])
    assert set(os.listdir(os.path.join(target_dir, 'songs'))) == set(['yesterday.txt', 'spanish', 'hungarian'])
    assert set(os.listdir(os.path.join(target_dir, 'songs', 'spanish'))) == set(['despacio.txt', 'rapido.txt'])
    assert set(os.listdir(os.path.join(target_dir, 'songs', 'hungarian'))) == set(['macska-az-uton.txt'])

    assert os.path.exists(os.path.join(target_dir, '.git', 'HEAD'))



    # Check if we deal with the removal of files and directories properly?
    with open(os.path.join(source_dir, 'songs', 'spanish', 'fast.txt'), 'w') as fh:
       fh.write('Fast!')
    os.remove(os.path.join(source_dir, 'songs', 'spanish', 'rapido.txt'))
    shutil.rmtree(os.path.join(source_dir, 'songs', 'hungarian'))

    bck = Backup()
    bck.main()
    assert set(os.listdir(target_dir)) == set(['.git', 'songs', 'a.txt'])
    assert set(os.listdir(os.path.join(target_dir, 'songs'))) == set(['yesterday.txt', 'spanish'])
    assert set(os.listdir(os.path.join(target_dir, 'songs', 'spanish'))) == set(['despacio.txt', 'fast.txt'])
    assert os.path.exists(os.path.join(target_dir, '.git', 'HEAD'))


def test_multi_dir_backup(tmpdir):
    tmp_dir = os.path.join(str(tmpdir), '2')  # Needed for Python 3.5 and older
    os.mkdir(tmp_dir)
    print('dir {}'.format(tmp_dir))
    source_dir = os.path.join(tmp_dir, 'src')
    target_dir = os.path.join(tmp_dir, 'target')
    config_file = os.path.join(tmp_dir, 'cfg.json')
    os.mkdir(source_dir)
    os.mkdir(target_dir)

    src_dir_1 = os.path.join(source_dir, 'someplace')
    trg_dir_1 = 'some_backup'
    os.mkdir(src_dir_1)
    with open(config_file, 'w') as fh:
       json.dump({
           'pairs': [
               {
                   "src": src_dir_1,
                   "trg": trg_dir_1,
               }
           ],
          'target': target_dir,
       }, fh)

    # pretend the git repository
    os.mkdir(os.path.join(target_dir, '.git'))
    with open(os.path.join(target_dir, '.git', 'HEAD'), 'w') as fh:
       fh.write('head')


    sys.argv = ['backup', '--config', config_file]
    bck = Backup()
    bck.main()
    assert set(os.listdir(target_dir)) == set(['.git', 'some_backup'])


    with open(os.path.join(src_dir_1, 'a.txt'), 'w') as fh:
       fh.write('hello')

    bck = Backup()
    bck.main()
    assert set(os.listdir(target_dir)) == set(['.git', 'some_backup'])
    assert set(os.listdir(os.path.join(target_dir, 'some_backup'))) == set(['a.txt'])


