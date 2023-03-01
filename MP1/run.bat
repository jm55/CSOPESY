@echo off

cls

echo =======================================
echo FCFS W/O IDLE 1
py driver.py < test_files\fcfs\fcfs_wo_idle_1.txt

echo =======================================
echo FCFS W/O IDLE 2    
py driver.py < test_files\fcfs\fcfs_wo_idle_2.txt

echo =======================================
echo FCFS W/O IDLE 3
py driver.py < test_files\fcfs\fcfs_wo_idle_3.txt

echo =======================================
echo FCFS W/ IDLE 1
py driver.py < test_files\fcfs\fcfs_w_idle_1.txt

echo =======================================
echo FCFS W/ IDLE 2
py driver.py < test_files\fcfs\fcfs_w_idle_2.txt

echo =======================================
echo SJF W/O IDLE 1
py driver.py < test_files\sjf\sjf_wo_idle_1.txt

echo =======================================
echo SJF W/O IDLE 2
py driver.py < test_files\sjf\sjf_wo_idle_2.txt

echo =======================================
echo SJF W/O IDLE 3
py driver.py < test_files\sjf\sjf_wo_idle_3.txt

echo =======================================
echo SJF W/ IDLE 1
py driver.py < test_files\sjf\sjf_w_idle_1.txt

echo =======================================
echo SJF W/ IDLE 2
py driver.py < test_files\sjf\sjf_w_idle_2.txt

echo =======================================
echo STRF W/O IDLE 1
py driver.py < test_files\strf\strf_wo_idle_1.txt

echo =======================================
echo STRF W/O IDLE 2
py driver.py < test_files\strf\strf_wo_idle_2.txt

echo =======================================
echo STRF W/ IDLE 1
py driver.py < test_files\strf\strf_w_idle_1.txt

echo =======================================
echo STRF W/ IDLE 2
py driver.py < test_files\strf\strf_w_idle_2.txt

echo =======================================
echo STRF W/ IDLE 3
py driver.py < test_files\strf\strf_w_idle_3.txt