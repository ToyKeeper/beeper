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
    print_hz_to_notes = True

    notes = []
    ms = 200
    vol = 1.0 / 5
    style = 'square'

    # by default, just make a beep
    if not args:
        notes.append(Note(style='tri', vol=vol))

    i = -1
    while (i+1) < len(args):
        i += 1
        a = args[i]

        if a in ('-h', '--help'):
            return help()

        elif a in ('-f', '--freq'):
            i += 1 ; a = args[i]
            hz = float(a)
            notes.append(Note(hz=hz, ms=ms, style=style, vol=vol))

            if print_hz_to_notes:
                num = freq2note(hz)
                rounded = int(round(num, 0))
                octave = int(rounded / 12)
                name = notenum2name[rounded % 12]
                name = '%s%s' % (name, octave)
                print('%.2f hz == note %.2f: %s' % (hz, num, name,))

        elif a in ('-n', '--note'):
            i += 1 ; a = args[i]
            notename = a
            note = Note(ms=ms, style=style, vol=vol)
            note.note(notename)
            notes.append(note)

        elif a in ('-l', '--len', '--length'):
            i += 1 ; a = args[i]
            ms = float(a)
            if notes:
                notes[-1].ms = ms

        elif a in ('-w', '--wave'):
            i += 1 ; a = args[i]
            st = a
            fname = '%s_wave' % (st)
            if fname not in globals():
                print('invalid wave style: %s' % (st,))
                return help()

            style = st
            if notes:
                notes[-1].style = style

        elif a in ('-d', '-D'):
            i += 1 ; a = args[i]
            d = float(a)
            notes.append(Note(hz=1, ms=d, style='square', vol=0))

        elif a in ('-v',):
            i += 1 ; a = args[i]
            vol = float(a) / 500.0
            if vol < 0.0: vol = 0.0
            if vol > 1.0: vol = 1.0
            if notes:
                notes[-1].vol = vol

        elif a in ('-c', '--cache'):
            cache = True

    # ensure beginning and end sound snappy
    stop = Note(hz=1, ms=0.1, vol=0)
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
    def __init__(self, hz=440, ms=200, style='square', vol=1.0):
        self.hz = hz
        self.ms = ms
        self.style = style
        self.vol = vol
        # avoid clicks between notes
        Note.phase = 0.0

    def note(self, name):
        num = notename2notenum(name)
        freq = note2freq(num)
        self.hz = freq

    def __str__(self):
        return 'Note(hz=%.1f, ms=%.1f, style=%s, vol=%.1f%%)' % (
                self.hz, self.ms, self.style, 100 * self.vol)

    def render(self, rate=44100):
        wave = globals()['%s_wave' % (self.style,)]

        num_samples = int(rate * self.ms / 1000)
        samples = bytearray(2 * num_samples)

        period = rate / float(self.hz)
        count = Note.phase * period
        j = 0
        for i in range(num_samples):
            if count > period:
                count -= period
            phase = count / period
            sample = int(wave(phase) * 32767 * self.vol)
            sample = sample.to_bytes(2, 'little', signed=True)
            samples[j] = sample[0]
            samples[j+1] = sample[1]
            j += 2
            count += 1

        # avoid clicks between notes
        Note.phase = phase
        if self.vol == 0.0:
            Note.phase = 0.0

        return samples


def render(path, notes):
    with wave.open(path, 'wb') as fp:
        fp.setnchannels(1)  # mono
        fp.setsampwidth(2)  # 16-bit audio
        fp.setframerate(44100)  # 44.1 kHz
        for note in notes:
            #print(note)
            fp.writeframes(note.render())


def play(path):
    os.system('play -q %s' % (path,))


def triangle_wave(phase):
    # /\
    #   \/
    if phase < 0.25:
        return phase * 4
    elif phase < 0.75:
        return 1.0 - (4*(phase-0.25))
    else:
        return ((phase-0.75) * 4) - 1.0
tri_wave = triangle_wave


def sawtooth_wave(phase):
    return 1.0 - (2 * phase)
saw_wave = sawtooth_wave


def square_wave(phase):
    if phase > 0.5:
        return 1.0
    return -1.0
sq_wave = square_wave


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


notenum2name = [
        'C', 'C+', 'D', 'D+', 'E', 'F', 'F+', 'G', 'G+', 'A', 'A+', 'B',
        ]
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

