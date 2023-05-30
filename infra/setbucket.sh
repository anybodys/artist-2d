#!/bin/bash

tf_file="main.tf"
tmpfile=$(mktemp)
cp --attributes-only --preserve $tf_file $tmpfile
cat $originalfile | envsubst > $tmpfile && mv $tmpfile $tf_file
