@echo off

cls

echo FCFS WITHOUT IDLE
py FCFS.py < wo_idle.txt

echo ===============

echo FCFS WITH IDLE
py FCFS.py < w_idle.txt