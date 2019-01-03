import json
import os
import sys

import backup

# create a temporary directory for the source files
# create a temp directory for the git repository
# run the backup
# check the results
#backup.run()
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
    backup.main()
    assert True
