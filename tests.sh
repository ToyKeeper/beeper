#!/bin/sh

if [ x"$1" = x"-v" ]; then
  VERBOSE=1
fi

B=./beeper.py

main () {
  style=square

  echo kick-1
  b 8000 -w tri -l 5 -v 100 20 -w sq -l 1 -v 200 -d 1
  echo kick-2
  b 12000 -w sq -l 5 -v 100 20 -w sq -l 1 -v 200 -d 1
  echo kick-3
  b 8000 -v 100 -w tri -l 0.3 18870 15725 13104 10920 9100 7583 6319 5266 4388 3657 3047 2539 2116 1763 1469 1224 1020 850 708 590 492 410 341 284 237 197 164 137 114 95 79 66 55 46 38 31 -l 2.2 -d 0.5

  echo tri-square-saw
  b -l 750 -n C4 -w tri -n C4 -w square -n C4 -w saw

  for style in square saw tri ; do
    echo "=== $style ==="
    echo volume test
    b -l 333 C5 -v 1 C5 -v 3 C5 -v 10 C5 -v 33 C5 -v 100 C5 -v 200 C5 -v 500
    echo AC power plugged in
    b -f 880 -l 50 -f 1200 -l 50
    echo AC power unplugged
    b -f 880 -l 50 -f 600 -l 50
    echo on-battery-power
    b -l 30 2000 500
    echo 1up
    b -l 50 -f 200 -f 400 -f 600 -f 800 -f 1000 -f 1200 -f 1600
    echo minor-lo
    b -l 50 -n B4 -D 20 -n D5 -D 20 -n F+5
    echo minor-hi
    b -l 50 -n E6 -D 20 -n G6 -D 20 -n B6
    echo minor-hi-back
    b -l 40 E6 G6 B6 G6 E6
    echo minor-hi-2
    b -l 30 -n C+6 -D 10 -n E6 -D 10 -n G+6 -D 10 -n C+6 -D 10 -n E6 -D 10 -n G+6
    b -l 40 C+6 E6 G+6 C+6 E6 G+6
    echo minor-arpeggio
    b -l 12 C+6 E6 G+6  C+6 E6 G+6  C+6 E6 G+6  C+6 E6 G+6
    echo major-lo
    b -l 50 B4 -d 20 D+5 -d 20 F+5
    echo major-hi
    b -l 50 E6 -D 20 G+6 -D 20 B6
    echo major-hi-back
    b -l 30 E6 -D 10 G+6 -D 10 B6 -D 10 G+6 -D 10 E6
    echo slip-down
    b -l 20 E6 -D 5 D+6 -D 5 D6 -D 5 C+6 -D 5 C6
    echo slip-down-short
    b -l 20 E6 -D 5 D+6 -D 5 D6
    echo slip-up
    b -l 20 D+6 -D 5 E6 -D 5 F6 -D 5 F+6 -D 5 G6 -D 5 G+6
    echo slip-up-short
    b -l 20 D+6 -D 5 E6 -D 5 F6
    echo random1
    b -l 30 -f 1527 -D 5 -f 2153 -D 5 -f 1721 -D 5 -f 1254 -D 5 -f 2153
    echo slide-up
    b -l 7 E4 F+4 G+4 A+4 C+5 E5 F+5 G+5 A+5 C6 D6 D+6 E6 F6
    echo red alert
    b -l 1 $(seq 100 1000)
    echo laser
    b -l 0.5 $(seq 1000 -1 100)
    echo ufo
    #b -l 0.5 $(seq 4000 -2 2000) $(seq 2000 2 4000) $(seq 4000 -2 2000) $(seq 2000 2 4000)
    b -l 1 $(seq 4000 -5 2000) $(seq 2000 5 4000) $(seq 4000 -5 2000) $(seq 2000 5 4000)
    echo pacman
    b -l 0.25 $(seq 4000 -5 2000) $(seq 2000 5 4000) $(seq 4000 -5 2000) $(seq 2000 5 4000)
    echo big blues scale
    b -l 100 \
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
  if [ ! -z "$VERBOSE" ]; then
    echo "$B -w $style $*"
  fi
  $B -w $style $*
  sleep 0.5
}

main
