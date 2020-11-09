./stop.sh
nohup erl -noshell -sname storage_prime -setcookie kolacic &
nohup erl -noshell -sname storage_composite -setcookie kolacic &
nohup erl -noshell -sname worker_1 -setcookie kolacic &
nohup erl -noshell -sname worker_2 -setcookie kolacic &
nohup erl -noshell -sname scheduler -setcookie kolacic &
erl -compile dz.erl
erl -sname x -setcookie kolacic -run dz start_system
