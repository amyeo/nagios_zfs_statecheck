# Nagios ZFS State Checker
Nagios plugin for checking ZFS pool state.
This plugin checks if the pool state is "ONLINE". If not, it sends back a critical status informing that the pool may be unavailable, degraded, etc.

Made with python3 using minimal amount of dependencies

## Example
```bash
$ ./check_zfs.py sample_pool
OK: Status ONLINE.
```
