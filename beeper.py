#!/usr/bin/env python3

# Like the "beep" command, but uses arbitrary playback program
# instead of the PC speaker.
# Because on many computers, the PC speaker doesn't work.


import math
import os
import wave


def main(args):
    """
    """

    tempfile = 'beeper.wav'
    cache = False

    notes = []
    last_was_new = False
    ms = 200
    vol = 0.25

    i = -1
    while (i+1) < len(args):
        i += 1
        a = args[i]

        if a in ('-h', '--help'):
            return help()

        elif a in ('-n', '--new'):
            last_was_new = True
            notes.append(Note(ms=ms, vol=vol))

        elif a in ('-f',):
            i += 1 ; a = args[i]
            hz = float(a)
            if last_was_new:
                notes[-1].hz = hz
            else:
                notes.append(Note(hz=hz, ms=ms, vol=vol))
            last_was_new = False

        elif a in ('-t', '--note'):
            i += 1 ; a = args[i]
            notename = a
            if last_was_new:
                notes[-1].note(notename)
            else:
                note = Note(ms=ms, vol=vol)
                note.note(notename)
                notes.append(note)
            last_was_new = False

        elif a in ('-l',):
            i += 1 ; a = args[i]
            ms = float(a)
            if notes:
                notes[-1].ms = ms

        elif a in ('-d', '-D'):
            i += 1 ; a = args[i]
            d = float(a)
            notes.append(Note(hz=1, ms=d, vol=0))

        elif a in ('-v',):
            i += 1 ; a = args[i]
            vol = float(a) / 200.0
            if vol < 0.0: vol = 0.0
            if vol > 1.0: vol = 1.0
            if notes:
                notes[-1].vol = vol

        elif a in ('-c', '--cache'):
            cache = True

    # ensure beginning and end sound snappy
    stop = Note(1, 0.1, 0)
    notes = [stop] + notes + [stop]

    outfile = tempfile

    if not cache:
        render(outfile, notes)

    else:
        # render to our sound cache
        path = 'beeper.%s.wav' % ('_'.join(args))
        outfile = os.path.join(os.environ['HOME'], '.sounds', path)
        #print(outfile)

        if not os.path.exists(outfile):
            render(outfile, notes)

    play(outfile)


def help(*args, **kwargs):
    print(main.__doc__)


class Note:
    def __init__(self, hz=440, ms=200, vol=1.0):
        self.hz = hz
        self.ms = ms
        self.vol = vol

    def note(self, name):
        num = notename2notenum(name)
        freq = note2freq(num)
        self.hz = freq

    def __str__(self):
        return 'Note(hz=%.1f, ms=%.1f)' % (self.hz, self.ms)

    def render(self, rate=44100):
        lo, hi = 0, 255
        mid = (hi+lo) / 2.0
        depth = (hi-lo) / 2.0
        sq = [int(mid - (depth*self.vol)), int(mid + (depth*self.vol))]
        sq = tuple(sq)
        flip = 0
        #samples = [int(mid)] + [sq[flip]] * int(rate * self.ms / 1000)
        samples = [sq[flip]] * int(rate * self.ms / 1000)
        period = rate / float(self.hz) / 2.0
        count = 0.0
        for i in range(len(samples)):
            samples[i] = sq[flip]
            if count > period:
                flip ^= 1
                count -= period
            count += 1
        b = bytes(samples)
        return b
        #return samples


def render(path, notes):
    with wave.open(path, 'wb') as fp:
        fp.setnchannels(1)  # mono
        fp.setsampwidth(1)  # 8-bit audio
        fp.setframerate(44100)  # 44.1 kHz
        for note in notes:
            #print(note)
            fp.writeframes(note.render())


def play(path):
    os.system('play -q %s' % (path,))


def notename2notenum(name):
    assert(name[:-1] in notenames)
    assert(int(name[-1]) >= 0)

    octave = int(name[-1])
    base = notenames[name[:-1]]
    num = (octave*12) + base
    return num


def note2freq(note):
    """Convert a midi note number into a frequency in Hz"""
    freq = 440.0 * math.pow(2, (note-57) / 12.0)
    return freq


def freq2note(freq):
    """Convert a frequency in Hz into a midi note number"""
    note = 57 + (12.0 * math.log(freq / 440.0, 2))
    return note


notenames = {
        'C' : 0,

        'C#': 1,
        'C+': 1,
        'D-': 1,
        'Db': 1,

        'D' : 2,

        'D#': 3,
        'D+': 3,
        'E-': 3,
        'Eb': 3,

        'E' : 4,

        'F' : 5,

        'F#': 6,
        'F+': 6,
        'G-': 6,
        'Gb': 6,

        'G' : 7,

        'G#': 8,
        'G+': 8,
        'A-': 8,
        'Ab': 8,

        'A' : 9,

        'A#': 10,
        'A+': 10,
        'B-': 10,
        'Bb': 10,

        'B' : 11,
        }


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])

