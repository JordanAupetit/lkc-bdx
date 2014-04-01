#!/bin/bash

path=$HOME/espaces/travail
lnx=3.13.5

if [ "$USER" = "fberarde" ]
then
    lnx=3.13.3
elif [ "$USER" = "mlemasso" ]
then
    lnx=3.13.5
elif [ "$USER" = "oxyasis" ]
then
    path="/home/oxyasis/git"
    lnx=3.13.6
fi

./app_render_gtk.py $path/linux-$lnx/ x86 x86_64_defconfig
find . -name "*.pyc" -exec rm -f {} \; -o -name "*~" -exec rm -f {} \;
