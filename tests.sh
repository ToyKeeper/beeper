#!/bin/sh

B=./beeper.py

main () {
  style=square
  b -l 750 -n C4 -w tri -n C4 -w square -n C4 -w saw

  for style in square saw tri ; do
    echo volume test
    b -l 500 -n C5 -v 1 -n C5 -v 10 -n C5 -v 100 -n C5 -v 500
    echo AC power plugged in
    b -f 880 -l 50 -f 1200 -l 50
    echo AC power unplugged
    b -f 880 -l 50 -f 600 -l 50
    echo 1up
    b -l 50 -f 200 -f 400 -f 600 -f 800 -f 1000 -f 1200
    echo minor-lo
    b -l 50 -f 500 -D 20 -f 600 -D 20 -f 750
    echo minor-hi
    b -l 50 -f 1308 -D 20 -f 1555 -D 20 -f 1959
    echo minor-hi-back
    b -l 30 -f 1308 -D 10 -f 1555 -D 10 -f 1959 -D 10 -f 1555 -D 10 -f 1308
    echo minor-hi-2
    b -l 30 -f 1100 -D 10 -f 1308 -D 10 -f 1648 -D 10 -f 1100 -D 10 -f 1308 -D 10 -f 1648
    echo minor-arpeggio
    b -l 12 -f 1100 -f 1308 -f 1648 -f 1100 -f 1308 -f 1648 -f 1100 -f 1308 -f 1648 -f 1100 -f 1308 -f 1648
    echo major-lo
    b -l 50 -f 500 -D 20 -f 625 -D 20 -f 750
    echo major-hi
    b -l 50 -f 1308 -D 20 -f 1648 -D 20 -f 1959
    echo major-hi-back
    b -l 30 -f 1308 -D 10 -f 1648 -D 10 -f 1959 -D 10 -f 1648 -D 10 -f 1308
    echo slip-down
    b -l 20 -f 1308 -D 5 -f 1234 -D 5 -f 1165 -D 5 -f 1100 -D 5 -f 1038
    echo slip-down-short
    b -l 20 -f 1308 -D 5 -f 1234 -D 5 -f 1165
    echo slip-up
    b -l 20 -f 1234 -D 5 -f 1308 -D 5 -f 1385 -D 5 -f 1468 -D 5 -f 1555 -D 5 -f 1648
    echo slip-up-short
    b -l 20 -f 1234 -D 5 -f 1308 -D 5 -f 1385
    echo random1
    b -l 30 -f 1527 -D 5 -f 2153 -D 5 -f 1721 -D 5 -f 1254 -D 5 -f 2153
    echo slide-up
    b -l 7 -f 327 -f 367 -f 412 -f 462 -f 550 -f 654 -f 734 -f 824 -f 924 -f 1038 -f 1165 -f 1234 -f 1308 -f 1385
    echo big blues scale
    b -l 100 \
      -n C1 -n D+1 -n F1 -n F+1 -n G1 -n A+1 \
      -n C2 -n D+2 -n F2 -n F+2 -n G2 -n A+2 \
      -n C3 -n D+3 -n F3 -n F+3 -n G3 -n A+3 \
      -n C4 -n D+4 -n F4 -n F+4 -n G4 -n A+4 \
      -n C5 -n D+5 -n F5 -n F+5 -n G5 -n A+5 \
      -n C6 -n D+6 -n F6 -n F+6 -n G6 -n A+6 \
      -n C7 -n D+7 -n F7 -n F+7 -n G7 -n A+7 -n C8
  done
}

b () {
  echo "$B -w $style $*"
  $B -w $style $*
  sleep 0.5
}

main
