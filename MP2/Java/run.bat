@echo off
cls
echo Script: run.bat

echo Compiling...
javac Driver.java

echo Running...
java Driver.java < sample_input.txt