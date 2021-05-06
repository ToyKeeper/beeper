#!/usr/bin/env python3

# beeper.py
# Like the "beep" command, but uses arbitrary playback program
# instead of the PC speaker.
# Because on many computers, the PC speaker doesn't work.
#
# Copyright (C) 2021 Selene ToyKeeper
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import math
import os
import subprocess
import wave


samplerate = 44100


def main(args):
    """beeper.py: make "PC speaker" noises ... without a PC speaker
    Usage: beeper.py [options] [tones]
    Options:
      -h    --help   Display usage info, and exit.
      -f F  --freq   Start a new note with Hz frequency F
      -n N  --note   Start a new note with name N
      -l L  --len    Set length of last note to L ms
      -w W  --wave   Set waveform of last note to W: [square] / saw / tri
      -v V  --vol    Set volume of last note to V percent [100] (max 500)
      -d D  --delay  Add a silent delay of length D ms
      -x X  --exec   Use program X to play the generated .wav file [aplay -q]
      -o F  --out    Save audio in .wav format to file F [beeper.wav]
      -c    --cache  Save .wav file to ~/.sounds/beeper.ARGS.wav
      -p    --print-conversions
                     Print frequency of each note, and note of each frequency

    Tones:  Can be a number or a note name.  "-f" and "-n" aren't required.
      Number: Add note of frequency N.  Range: 1.0 to 22050.0
      Name:   Add note of a given name.  Range: C0 to B9
              Sharps can be '+' or '#', flats can be '-' or 'b'.
              For example: G+4 Eb6

    Examples:

    Play a triumphant jingle:
      beeper.py C4 -l 100 -d 30 E4 -d 30 G4 -d 30 C5 -l 200 -d 30 \\
                G4 -l 100 -d 30 C5 -l 200

    Play a retro arpeggio:
      beeper.py -w tri -l 40 C4 E4 G4 C5 E5 G5 C6 E6 G6 C7 \\
                                G6 E6 C6 G5 E5 C5 G4 E4 C4

    Red alert, Captain!
      beeper.py -w saw -l 1 $(seq 100 1000)
    """

    outfile = 'beeper.wav'
    cache = False
    print_conversions = False
    play_cmd = 'aplay -q'  # alsa default .wav player

    notes = []
    ms = 200
    vol = 1.0 / 5
    style = 'square'

    def freq_opt(a):
        hz = float(a)
        notes.append(Note(hz=hz, ms=ms, style=style, vol=vol))

        if print_conversions:
            num = freq2note(hz)
            rounded = int(round(num, 0))
            octave = int(rounded / 12)
            name = notenum2name[rounded % 12]
            name = '%s%s' % (name, octave)
            print('%8.2f hz == note %6.2f: %s' % (hz, num, name,))

    def note_opt(a):
        notename = a
        note = Note(ms=ms, style=style, vol=vol)
        note.note(notename)
        notes.append(note)

        if print_conversions:
            name = notename
            num = note.notenum
            hz = note.hz
            print('%-3s == note %6.2f == %8.2f hz' % (name, num, hz))

    i = -1
    while (i+1) < len(args):
        i += 1
        a = args[i]

        if not a.strip():
            continue

        if a in ('-h', '--help'):
            return help()

        elif a in ('-f', '--freq'):
            i += 1 ; a = args[i]
            freq_opt(a)

        elif a in ('-n', '--note'):
            i += 1 ; a = args[i]
            note_opt(a)

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

        elif a in ('-d', '-D', '--delay'):
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

        elif a in ('-x', '--exec'):
            i += 1 ; a = args[i]
            play_cmd = a

        elif a in ('-o', '--out'):
            i += 1 ; a = args[i]
            outfile = a

        elif a in ('-c', '--cache'):
            cache = True

        elif a in ('-p', '--print-conversions'):
            print_conversions = True

        else:
            if a[0] in '0123456789':
                freq_opt(a)
            elif a[0] in 'CDEFGAB':
                note_opt(a)
            else:
                print('Unrecognized option: %s' % a)
                return help()

    # by default, just make a beep
    if not notes:
        notes.append(Note(style=style, ms=ms, vol=vol))

    # ensure beginning and end sound snappy
    #stop = Note(hz=1, ms=0.1, vol=0)
    #notes = [stop] + notes + [stop]

    if not cache:
        render(outfile, notes)

    else:
        # render to our sound cache
        path = 'beeper.%s.wav' % ('_'.join(args))
        # don't try to make the filename longer than the filesystem allows
        maxlen = 248
        if len(path) > maxlen:
            path = path[:maxlen] + '.wav'

        outfile = os.path.join(os.environ['HOME'], '.sounds', path)

        if os.path.exists(outfile):
            print('Used cached file: %s' % (outfile,))
        else:
            render(outfile, notes)
            print('Cached to: %s' % (outfile,))

    play(outfile, play_cmd)


def help(*args, **kwargs):
    text = main.__doc__.replace('\n    ', '\n')
    print(text)


class Note:
    def __init__(self, hz=440, ms=200, style='square', vol=1.0):
        self.hz = hz
        self.ms = ms
        self.style = style
        self.vol = vol
        # avoid clicks between notes
        Note.phase = 0.0

    def note(self, name):
        """Set frequency by note name."""
        self.notenum = notename2notenum(name)
        freq = note2freq(self.notenum)
        self.hz = freq

    def __str__(self):
        return 'Note(hz=%.1f, ms=%.1f, style=%s, vol=%.1f%%)' % (
                self.hz, self.ms, self.style, 100 * self.vol)

    def render(self, rate=samplerate):
        wave = globals()['%s_wave' % (self.style,)]

        num_samples = int(rate * self.ms / 1000)
        samples = bytearray(2 * num_samples)

        period = rate / float(self.hz)
        count = Note.phase * period
        for i in range(num_samples):
            if count > period:
                count -= period
            phase = count / period
            sample = int(wave(phase) * 32767 * self.vol)
            sample = sample.to_bytes(2, 'little', signed=True)
            samples[   2*i ] = sample[0]
            samples[1+(2*i)] = sample[1]
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
        fp.setframerate(samplerate)  # 44.1 kHz (probably)
        for note in notes:
            #print(note)
            fp.writeframes(note.render())


def run(*args):
    proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = str(proc.stdout, encoding='utf-8')
    stderr = str(proc.stderr, encoding='utf-8')
    code = proc.returncode
    return code, stdout, stderr


def play(path, play_cmd):
    parts = play_cmd.split()
    parts.append(path)
    run(*parts)


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

