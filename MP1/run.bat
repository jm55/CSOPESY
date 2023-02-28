@echo off

cls

echo FCFS W/O IDLE 1
py driver.py < test_files\fcfs_wo_idle_1.txt

echo =======================================

echo FCFS W/O IDLE 2
py driver.py < test_files\fcfs_wo_idle_2.txt

echo =======================================

echo FCFS W/ IDLE 1
py driver.py < test_files\fcfs_w_idle_1.txt