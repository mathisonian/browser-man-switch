browser-man-switch
==================

A Dead Man's Switch to clear your browser history on OSX.

NOTE: Currently only works with Chrome

Intro
-----

This is a python script that periodically checks the last time you've used a web browser. If that time is
greater than a certain threshold, you are presumed dead, and any browser history is deleted, to make sure that
loved ones don't see any... ahem... unpleasantries on your computer.

Usage
-----

### Installation

First checkout this repository to a nice place. Then clone it with 

```
git clone git://github.com/mathisonian/browser-man-switch.git
```

Move into that directory with ```cd browser-man-switch``` and you are ready to start.

### Running

This is a command line python program. Run like so:

```
python history-cleaner.py --chrome --length 7 --daemon
```

This will cause the process to start in the background as a daemon, clearing my chrome history if I don't
login for 7 or more days. 

### Options

* `length` - Time in days to wait before assuming you are dead. Can be fractional (eg `7.5`)
* `chrome` - Actively monitor chrome
* `firefox` - Actively monitor firefox
* `safari` - Actively monitor safari
* `daemon` - Run as a background process. Defaults to foreground mode.

If one of `chrome`, `firefox`, or `safari`, is not flagged, chrome will be assumed. You can do any combination of the three.

Running on Startup
---

It is important that you have this setup to run on startup. To do so, add the following to your crontab file (stored in `/etc/crontab`). Make sure to edit as root.

```
@reboot python /path/to/history-cleaner.py <options>
```
