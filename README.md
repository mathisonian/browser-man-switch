browser-man-switch
==================

A [Dead Man's Switch](http://en.wikipedia.org/wiki/Dead_man's_switch) to clear your browser history on OSX.
*Note: Currently only works with Chrome*



> If she murders me, tell Jean-Ralphio to clear my browser history.
>
> -- Tom Haverford



Intro
-----

This is a python script that periodically checks the last time you've used a web browser. If that time is
greater than a certain threshold, you are presumed dead, and any browser history is deleted. 

Usage
-----

### Installation

Clone this repository to a nice place with 

```
git clone git://github.com/mathisonian/browser-man-switch.git
```

Move into that directory with ```cd browser-man-switch``` and you are ready to start.

### Running

This is a command line python program. Run like so:

```
python history-cleaner.py --chrome --time 7 --daemon
```

This will cause the process to start in the background as a daemon, clearing your chrome history if chrome isn't used for 7 or more days. 

### Options

* `time` - Time in days to wait before assuming you are dead. Can be fractional (eg `7.5`). Defaults to 7 days
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

Author
----
* Matthew Conlen, http://www.mathisonian.com


License
----
Copyright © 2013 Matthew Conlen

This program is free software. It comes without any warranty, to the extent permitted by applicable law. You can redistribute it and/or modify it under the terms of the WTFPL, Version 2, as published by Sam Hocevar. See http://sam.zoy.org/wtfpl/ for more details.
