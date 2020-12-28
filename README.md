# Simple Nagios ZFS State Checker (no root)
Nagios plugin for checking ZFS pool state.
This plugin checks if the pool state is "ONLINE". If not, it sends back a critical status informing that the pool may be unavailable, degraded, etc.

Made with python3 using minimal amount of dependencies. This does not need root to run.
By simple, it just parses "zpool status <pool name>". 

## Example
```bash
$ ./check_zfs.py sample_pool
OK: Status ONLINE.
```
