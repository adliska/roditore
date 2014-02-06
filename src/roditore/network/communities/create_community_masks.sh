#!/bin/bash

while getopts "i:p:m:" opt
do
    case $opt in
        i)
            input=$OPTARG
            ;;
        p)
            prefix=$OPTARG
            ;;
        m)
            master=$OPTARG
            ;;
    esac
done

num_communities=`cut -f4 -d' ' $input | sort | uniq | wc -l`

for comm in $(seq 1 $num_communities)
do
    grep " ${comm}$" $input | \
        cut -f1-3 -d' ' | \
        ~/tools/afni64/3dUndump \
            -prefix ${prefix}_comm${comm}.nii.gz \
            -master $master \
            -
done
