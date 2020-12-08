Each folder contains one program for use on a hadoop cluster

To compile position yourself in the program folder and run:
javac -classpath ../hadoop-common-2.7.4.jar:../hadoop-mapreduce-client-core-2.7.4.jar -d classes *.java
jar -cvf Matrix.jar -C classes/ .

Copy the resulting jar file to namenode and run along with the log/dat file

