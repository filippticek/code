./stop.sh

#cd scheduler/
#erl -compile *
#cd ../storage_prime/
#erl -compile *
#cd ../storage_composite/
#erl -compile *
#cd ../worker_1/
#erl -compile *
#cd ../worker_2/
#erl -compile *
#cd ..
cd storage_prime
erl -detached -sname storage_prime -setcookie kolacic -eval "application:start(storageApp)" 
cd ../storage_composite
erl -detached -sname storage_composite -setcookie kolacic -eval "application:start(storageApp)" 
cd ../worker1
erl -detached -sname worker_1 -setcookie kolacic -eval "application:start(workerApp)" 
cd ../worker2
erl -detached -sname worker_2 -setcookie kolacic -eval "application:start(workerApp)" 
cd ../scheduler
erl -sname scheduler -setcookie kolacic -eval "application:start(schedulerApp)" 
./stop.sh
