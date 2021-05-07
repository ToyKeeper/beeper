#!/bin/sh

# tests / examples for beeper.py

if [ x"$1" = x"-v" ]; then
  VERBOSE=1
fi

B=./beeper.py

main () {

  echo "== misc sounds =="

  # [int(1.2**x)) for x in range(16, 55)].reverse()
  b kick-1 8000 -v 100 -w tri -l 0.3 18870 15725 13104 10920 9100 7583 6319 5266 4388 3657 3047 2539 2116 1763 1469 1224 1020 850 708 590 492 410 341 284 237 197 164 137 114 95 79 66 55 46 38 31 -l 2.2 -d 0.5
  b kick-2 8000 -w tri -l 5 -v 100 20 -w sq -l 1 -v 200 -d 1
  b kick-3 12000 -w sq -l 5 -v 100 20 -w sq -l 1 -v 200 -d 1

  b tri-square-saw -l 750 -n C4 -w tri -n C -w square -n C -w saw

  for style in square saw tri ; do

    echo "=== $style ==="

    b volume-test -l 333 C -v 1 C -v 3 C -v 10 C -v 33 C -v 100 C -v 200 C -v 500

    b ac-power-plugged-in -f 880 -l 50 -f 1200 -l 50
    b ac-power-unplugged -f 880 -l 50 -f 600 -l 50
    b on-battery-power -l 30 2000 500

    b 1up -l 50 -f 200 -f 400 -f 600 -f 800 -f 1000 -f 1200 -f 1600
    b minor-lo -l 50 -n B4 -D 20 -n D -D 20 -n F+
    b minor-hi -l 50 -n E6 -D 20 -n G -D 20 -n B
    b minor-hi-back -l 40 E6 G B G E
    b minor-hi-2 -l 30 -n C+6 -D 10 -n E6 -D 10 -n G+6 -D 10 -n C+6 -D 10 -n E6 -D 10 -n G+6
    b minor-hi-2b -l 40 C+6 E G+ C+6 E G+
    b minor-arpeggio -l 12 C+6 E G+  C+6 E G+  C+6 E G+  C+6 E G+
    b major-lo -l 50 B4 -d 20 D+ -d 20 F+
    b major-hi -l 50 E6 -D 20 G+ -D 20 B
    b major-hi-back -l 30 E6 -D 10 G+ -D 10 B -D 10 G+ -D 10 E
    b slip-down -l 20 E6 -D 5 D+ -D 5 D -D 5 C+ -D 5 C
    b slip-down-short -l 20 E6 -D 5 D+ -D 5 D
    b slip-up -l 20 D+6 -D 5 E -D 5 F -D 5 F+ -D 5 G -D 5 G+
    b slip-up-short -l 20 D+6 -D 5 E -D 5 F
    b random1 -l 30 -f 1527 -D 5 -f 2153 -D 5 -f 1721 -D 5 -f 1254 -D 5 -f 2153
    b slide-up -l 7 E4 F+ G+ A+ C+ E F+ G+ A+ C D D+ E F

    b red-alert -l 1 $(seq 100 1000)
    b laser -l 0.5 $(seq 1000 -1 100)
    b random -l 80 $(./randints.py 100 4000 16)
    # d'oh, the UFO sound got a lot less interesting when I fixed a bug..
    # ... because the cool sound it made depended on a bug in the synth engine
    # (it'd repeat the same phase for one sample each time a note started,
    #  which made audible artifacts, and the "ufo" sound was based on those)
    # so... it's boring now
    #b ufo -l 0.5 $(seq 4000 -2 2000) $(seq 2000 2 4000) $(seq 4000 -2 2000) $(seq 2000 2 4000)
    b ufo -l 1 $(seq 4000 -5 2000) $(seq 2000 5 4000) $(seq 4000 -5 2000) $(seq 2000 5 4000)
    b pacman -l 0.25 $(seq 4000 -5 2000) $(seq 2000 5 4000) $(seq 4000 -5 2000) $(seq 2000 5 4000)

    # C0 to C10
    b big-blues-scale -l 80 \
      C0 D+ F F+ G A+ \
      C  D+ F F+ G A+ \
      C  D+ F F+ G A+ \
      C  D+ F F+ G A+ \
      C  D+ F F+ G A+ \
      C  D+ F F+ G A+ \
      C  D+ F F+ G A+ \
      C  D+ F F+ G A+ \
      C  D+ F F+ G A+ \
      C  D+ F F+ G A+ C

  done

}

b () {
  NAME="$1" ; shift
  echo "  $NAME"

  # determine .wav file name and waveform style
  if [ -z "$style" ]; then
    OUTFILE="${NAME}.wav"
    EXTRA=''
  else
    OUTFILE="${NAME}.${style}.wav"
    EXTRA="-w $style"
  fi

  # maybe show a command the user can run to get this sound
  if [ ! -z "$VERBOSE" ]; then
    echo "$B $EXTRA $*"
  fi

  # make some noise
  $B -o "$OUTFILE" $EXTRA $*

  # pause betwene tests
  sleep 0.5
}

main
