@echo off

cls

echo SJF WITHOUT IDLE
py SJF.py < wo_idle.txt

echo ===============

echo SJF WITH IDLE
py SJF.py < w_idle.txt