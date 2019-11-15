#!/bin/bash
for file in "$PWD/.*.completion"; do
    source $file;
done
