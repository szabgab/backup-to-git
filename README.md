# Backup to Git

A simple script to back files to a git repository

[![Build Status](https://travis-ci.org/szabgab/backup-to-git.png)](https://travis-ci.org/szabgab/backup-to-git)


# Configuration

Here every file from `source` is copied to `target` and added to the git repository.
`target` is the root of a git repository.

```
{
	"source": "/home/foobar/someplace",
	"target": "/home/foobar/backup"
}
```

# Planned configuration:

Here `target` is still the root of the place where everything is copied to (and the git repository),
but now we have multiple sources, each with a target direcatory relative to the `target`.


Configuring with regexes:

```
{
    "pairs": [
        {
	        "src": "/home/foorbar/someplace",
            "trg": "someplace"
        },
        {
            "src": "/home/foobar/jenkins/(.*/config.xml)"
            "trg": "jenkins/$1"
        }
    ],
	"target": "/home/foobar/backup"
}

```

Configuring with extended wildcards where * can match anything that does not contain a slash and ** can match slashes as
well?


