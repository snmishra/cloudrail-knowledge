#!/bin/bash -eu

__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

sizethreshold=1048576
wlbinary="${__dir}/white-list-binary.txt"
wlsize="${__dir}/white-list-by-size.txt"

function ShowUsage
{
    cat <<EOF

Usage:

${0} {source branch} {destionation branch}

EOF
}

if [[ $# -ne 2 ]]; then
  echo "ERROR: Wrong parameters"
  ShowUsage
  exit 1
fi

if [[ ! -f "$wlbinary" ]]; then
    echo "$wlbinary does not exist"
    exit 1
fi

if [[ ! -f "$wlsize" ]]; then
    echo "$wlsize does not exist"
    exit 1
fi

commits=$(git --no-pager log --no-merges $1 --not $2 --pretty=format:"%H" --max-count=100)

fbinall=
findingsBig=
findingsBinary=


for line in $commits; do
    # --differ-filter=dr -> exclude deleted and renamed files
    filesinacommit=$(git --no-pager log -1 --diff-filter=dr --numstat --pretty="" $line | awk '$2 == "-" {print $3}' )
    # use echo command with double quotes to print with new lines
    filesinacommit=$(echo "${filesinacommit}" | grep -v -f ${wlbinary} || true)
    for fil in $filesinacommit; do
        fbinall="${fbinall}commit: ${line} file: ${fil}"$'\n'
    done
done

findingsBinary=$(echo "${fbinall}" | sort --unique)

for line in $commits; do
    for filename in $(git --no-pager log -1 --diff-filter=dr --numstat --pretty="" $line | awk '$2 == "-" {print $3}' | grep -v -f $wlsize); do
        filesize=$(git cat-file -s $line:$filename)
        if [[ $filesize -gt $sizethreshold ]]; then findingsBig="${findingsBig}commit: ${line} file: ${filename} size: ${filesize}"$'\n'; fi
    done
done

findingsSize=$(echo "$findingsBig" | sort --unique)

if [[ ! -z "$findingsBinary" ]]; then
    echo "========================================================================"
    echo -e "ERROR: Binary file(s) was found:\n$findingsBinary"
    echo "========================================================================"
fi

if [[ ! -z "$findingsSize" ]]; then
    echo "========================================================================"
    echo -e "ERROR: Big file(s) was found:\n$findingsSize"
    echo "========================================================================"
fi

if [[ ! -z "$findingsBinary" || ! -z "$findingsSize" ]]; then
    exit 1
fi
