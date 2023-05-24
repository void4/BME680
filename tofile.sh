cat /dev/ttyACM0 | perl -pne 'use POSIX qw(strftime); print strftime "%Y-%m-%dT%H:%M:%SZ ", gmtime(); select()->flush();
' | tee -a measurements.jsonl
