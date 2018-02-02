#!/usr/bin/env bash
# Linux 系统上启动 tclient 的脚本


ROOTDIR=$(dirname $0)
export PATH=${ROOTDIR}/python-2.7.14/bin:$PATH
alias python=${ROOTDIR}/python-2.7.14/bin/python

python $@ &
