#! /usr/bin/sh

# !!! IMPORTANT !!!
# Run this file from *within* the doc directory!

# Repopulate a wiped DB with the backed up data stored in the SQL files in this (doc) directory.
# The data it createes matches the data supplied in template-es.xlsx, used to test excel
# document uploading and parsing.

for file in `ls *.sql`;
  do mysql -u root -p rvd < $file;
done
