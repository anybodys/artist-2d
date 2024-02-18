#!/bin/bash

set -x
tf_file="main.tf"
tmpfile=$(mktemp)
cp --attributes-only --preserve $tf_file $tmpfile
cat $tf_file | envsubst > $tmpfile && mv $tmpfile $tf_file
