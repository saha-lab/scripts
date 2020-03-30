#!/bin/bash
## A wrapper bash script to be used with any blast program in order to monitor the progress of a blast.
## USAGE: blast_monitor.sh <blast_command_with_options>
## Updated 180721 by Ronald Cutler

die() {
  echo $1 >&2
  exit 1
}

## test whether the command is correct ##
[[ "$1" =~ blast* ]] || die "Not a blast program '$1'"
command -v "$1" >/dev/null 2>&1 || die "'$1' not found"

## grasp the -query argument to replace it with owr pipe ##
for ((j=$#;j>0;j--)); do
  if [ "${!j}" == '-query' ]; then
    i=$((j-1)); k=$((j+1)); l=$((j+2))
    query=${!k}
    set -- "${@:1:i}" "${@:l}"
    break
  fi
done

## validate the query ##
[ -f "$query" ] || die 'Input file not found'
lines=$(wc -l < "$query")
((lines>0)) || die 'Input file is empty'

## we need these two strings to plot the progress bar ##
bar='===================================================================================================='
blk='                                                                                                    '

echo "Lines consumed:" >&2
printf '[%.*s] %d %%\r' 100 "$blk" 0 >&2

## ival is the number of rows corresponding to 1% ##
ival=$((lines/100))
((ival==0)) && ival=1

## we use awk to monitor the number of lines consumed by blast ##
awk='{ print }
    NR%'$ival'==0 {
      p=sprintf("%.f", NR*100/'$lines');
      system("printf '"'[%.*s%.*s] %d %%\r'"' "p" '"'$bar'"' "(100-p)" '"'$blk'"' "p" >&2");
  }'

## run blast ##
eval "$@" -query <(awk "$awk" "$query")

echo >&2
echo 'Done' >&2