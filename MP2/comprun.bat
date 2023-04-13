@echo off

del *.class

cls
echo COMPILE AND RUN

echo Compiling...
javac Driver.java

echo Running...
java Driver.java < sample_input.txt