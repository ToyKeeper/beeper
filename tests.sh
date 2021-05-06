#!/bin/sh

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

  b tri-square-saw -l 750 -n C4 -w tri -n C4 -w square -n C4 -w saw

  for style in square saw tri ; do

    echo "=== $style ==="

    b volume-test -l 333 C5 -v 1 C5 -v 3 C5 -v 10 C5 -v 33 C5 -v 100 C5 -v 200 C5 -v 500

    b ac-power-plugged-in -f 880 -l 50 -f 1200 -l 50
    b ac-power-unplugged -f 880 -l 50 -f 600 -l 50
    b on-battery-power -l 30 2000 500

    b 1up -l 50 -f 200 -f 400 -f 600 -f 800 -f 1000 -f 1200 -f 1600
    b minor-lo -l 50 -n B4 -D 20 -n D5 -D 20 -n F+5
    b minor-hi -l 50 -n E6 -D 20 -n G6 -D 20 -n B6
    b minor-hi-back -l 40 E6 G6 B6 G6 E6
    b minor-hi-2 -l 30 -n C+6 -D 10 -n E6 -D 10 -n G+6 -D 10 -n C+6 -D 10 -n E6 -D 10 -n G+6
    b minor-hi-2b -l 40 C+6 E6 G+6 C+6 E6 G+6
    b minor-arpeggio -l 12 C+6 E6 G+6  C+6 E6 G+6  C+6 E6 G+6  C+6 E6 G+6
    b major-lo -l 50 B4 -d 20 D+5 -d 20 F+5
    b major-hi -l 50 E6 -D 20 G+6 -D 20 B6
    b major-hi-back -l 30 E6 -D 10 G+6 -D 10 B6 -D 10 G+6 -D 10 E6
    b slip-down -l 20 E6 -D 5 D+6 -D 5 D6 -D 5 C+6 -D 5 C6
    b slip-down-short -l 20 E6 -D 5 D+6 -D 5 D6
    b slip-up -l 20 D+6 -D 5 E6 -D 5 F6 -D 5 F+6 -D 5 G6 -D 5 G+6
    b slip-up-short -l 20 D+6 -D 5 E6 -D 5 F6
    b random1 -l 30 -f 1527 -D 5 -f 2153 -D 5 -f 1721 -D 5 -f 1254 -D 5 -f 2153
    b slide-up -l 7 E4 F+4 G+4 A+4 C+5 E5 F+5 G+5 A+5 C6 D6 D+6 E6 F6

    b red-alert -l 1 $(seq 100 1000)
    b laser -l 0.5 $(seq 1000 -1 100)
    #b ufo -l 0.5 $(seq 4000 -2 2000) $(seq 2000 2 4000) $(seq 4000 -2 2000) $(seq 2000 2 4000)
    b ufo -l 1 $(seq 4000 -5 2000) $(seq 2000 5 4000) $(seq 4000 -5 2000) $(seq 2000 5 4000)
    b pacman -l 0.25 $(seq 4000 -5 2000) $(seq 2000 5 4000) $(seq 4000 -5 2000) $(seq 2000 5 4000)

    b big-blues-scale -l 100 \
      C1 D+1 F1 F+1 G1 A+1 \
      C2 D+2 F2 F+2 G2 A+2 \
      C3 D+3 F3 F+3 G3 A+3 \
      C4 D+4 F4 F+4 G4 A+4 \
      C5 D+5 F5 F+5 G5 A+5 \
      C6 D+6 F6 F+6 G6 A+6 \
      C7 D+7 F7 F+7 G7 A+7 C8

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
