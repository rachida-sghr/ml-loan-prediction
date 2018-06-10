#!/bin/bash

GREEN="\\033[0;32m"
RED="\\033[0;31m"
NOCOLOR="\\033[0m"

# helpers to pretty print messages
info() {
    printf "${GREEN}[INFO]  %s${NOCOLOR}\\n" "$@"
}

err() {
    printf "${RED}[ERROR] %s${NOCOLOR}\\n" "$@" 1>&2
}

get_columns_perfomance(){
    local path=

    if [[ "$1" = /* ]]; then
        path="$1"
    else
        path="$(pwd)/$1"
    fi

    if [ -z "$path" ] ; then
        err "get_columns called without argument (or with an empty path as argument)" 
    fi 

    if [ ! -d "$path" ] ; then 
        err "path does not exist"
    fi
    
    local processed="$path"/processed
    rm -rf "$processed"
    mkdir "$processed"

    for f in "$path"/*.txt; do
        [[ -e $f ]] || break # handle the case of no *.txt files
        cut -d '|' -f 1,15 "$f" > "$processed"/"${f##*/}" # get id and foreclosure_date
    done
}

concat_files(){
    local path=

    if [[ "$1" = /* ]]; then
        path="$1"
    else
        path="$(pwd)/$1"
    fi

    if [ -z "$path" ] ; then
        err "get_columns called without argument (or with an empty path as argument)" 
    fi 

    if [ ! -d "$path" ] ; then 
        err "path does not exist"
    fi

    file_name=$(basename $path)
    echo "$file_name"
    rm -f ./processed/"$file_name".txt
    touch ./processed/"$file_name".txt

    for f in "$path"/processed/*.txt; do
        [[ -e $f ]] || break # handle the case of no *.txt files 
        cat ./processed/"$file_name".txt "$f" > tmpfile && mv tmpfile ./processed/"$file_name".txt
    done
}

set -x

if [[ $(basename "$1") = performance ]]; then
    get_columns_perfomance "$@"
    concat_files "$@"
fi

if [[ $(basename "$1") = acquisition ]]; then
    concat_files "$@"
fi


 