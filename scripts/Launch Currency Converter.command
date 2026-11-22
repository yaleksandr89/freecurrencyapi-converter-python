#!/bin/sh

trap 'exit 130' INT

CDPATH= cd -P -- "$(dirname "$0")" && ./currency-converter "$@"
status=$?

if [ "$status" -ne 130 ] && [ -t 0 ] && [ -t 1 ] && [ -t 2 ]; then
    printf '\nНажмите Enter, чтобы закрыть / Press Enter to close: '
    IFS= read -r unused
fi

exit "$status"
