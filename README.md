# Beeper

Like the "beep" command, but uses arbitrary playback program
instead of the PC speaker.

Because on many computers, the PC speaker is nonexistent or has been disabled
by the OS.


## Requirements

  * Python 3
  * A command-line .wav player, such as ALSA's "aplay"


## Example sounds

Run **tests.sh** to generate a bunch of example sounds.  Use **tests.sh -v** to
see the commands used to generate each one.


## Extra features

Compared to "beep", there are several new features:

  * Can adjust the volume.

  * Can play sawtooth and triangle waves, not just square waves.

  * Can specify tones by note name, not just frequency.

  * Can save .wav files for later use.

  * Can play sounds via the sound card instead of PC speaker.  Uses whatever
    media player command you specify.

  * Supports floating-point values for frequency, length, and volume.

  * Several parameters are available per note:
    * Frequency
    * Length
    * Volume
    * Wave shape

As a side note, a few options are implicit and don't need a "-a / --arg" before
them:

    * Frequency (-f)
    * Note name (-n)
    * Wave shape (-w)

... and other options generally carry forward and affect everything after them,
with no need to repeat the option.  So instead of this...

```
./beeper.py -n C5 -w square -l 100 -n E5 -w tri -l 100 -n G5 -w tri -l 100 -n C6 -w tri -l 100
```

... it also works to do this:

```
./beeper.py -l 100 C5 square E5 tri G5 C6
```


## X11 Bell

To make the X11 Bell work, install the xkbevd program and give it a simple
config file:

**~/.xkb/xkbevd.cf**
```
soundDirectory = "/home/myuser/.sounds/"
soundCmd = "aplay -q"

Bell() "x11-bell.wav"
```

Make sure you have a ".sounds" directory, of course... with a "x11-bell.wav"
file in it.  Try playing with "beeper.py" to generate a sound you like, then
copy it there.  Personally, I find the "kick-1" style from the "tests.sh"
script works well.

Once the sound and config are in place, start xkbevd in your **.Xsession** or similar
session file:

`xkbevd -bg`

It may be a little laggy compared to the native X11 beep.


## Porting scripts from the "beep" command

This program can mostly be used in place of "beep", but it has a few
differences to keep in mind when updating scripts:

  * **Don't use "-n" or "--new" between tones.**  Remove all those "-n"
    parameters your script was sending to "beep".  The "beeper.py" program
    starts a new tone automatically every time it detects a new frequency or
    note.  It doesn't even need "-f" first.  Just specify the frequency or the
    note name, and it'll start a new tone.

  * Many of "beep"'s parameters can be removed without consequence.  For
    example, if you play several tones of the same length, "beep" required
    specifying the length with "-l" each time.  However, "beeper.py" only needs
    it specified once and that length will be applied to every tone from then
    on.

  * The "-n" option is used to specify notes by name, like "C5" or "F+4", so it
    is important to remove the "-n" options from old scripts.  That option does
    something else now.

  * The "-r REPEATS" option isn't supported.

  * The input processing mode ("-s" and "-c") is not supported.

  * The "-p" or "--print-conversions" option may be useful for porting old
    scripts, since it shows the note name for each frequency, and the frequency
    for each note.


## Installation

Download the source.  Run "beeper.py".

Optionally put "beeper.py" somewhere in your `$PATH`.  For example:

```
cd ~/bin/
ln -s ~/src/beeper/beeper.py beeper
```

