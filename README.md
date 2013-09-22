Description
===========

This bot was written and designed for `mmcfe-ng`, specifically the API
supplied with `mmcfe-ng`. It was intended as a simple IRC solution to
notify users of new blocks and offer some commands to check the pool
status.

Requirements
============

* python-daemon

Installation
============

Download the source code via git. Ensure you have `python-daemon`
installed:

```
easy_install python-daemon
```

or via your distributions package repository, if available.

Configuration
=============

Copy the sample configuration file `conf/example.cfg` and replace settings as you see fit.

Running the Bot
===============

Execute the supplied python script to fork the process in the
background:

`./ejgithub.py`

Closing the Bot
===============

Kill the process ID via `kill` and remove the PID files afterward. This
shall be added as a cleanup call later down the road.

Adding Commands
===============

If you want to add your own commands please check the supplied ones
in the `commands` folder. They are simple to create and easy to add to
the bot.

* Create a new subfolder in `commands`, this will be your commands name
* Create a new file `__init__.py` in your commands subfolder
* Create a new `def yourcommand_run_cmd` which is called when your
  command is triggered (see samples supplied)
* Returned data of that command is send to the IRC channel

Reloading Commands
==================

Whenever you are working with commands you might want to re-load these
without re-starting the bot. You can do so by sending the `SIGUSR1`
signal to the process. It will re-hash all commands available and you
should be able to try them out or edit them anytime.

Blocknotify
===========

The bot does support coins blocknotify scripts. As with reloading
commands, send a `SIGUSR1` call to the process to enforce a blockupdate
request. Might be useful for those with very fast block finding rates.

License
=======

TBA
