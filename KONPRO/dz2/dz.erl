-module(dz).
-export([start_system/0, storage_init/1, worker_init/1, scheduler_init/0]).
-import(math, [pow/2]).

%Storage node initialization and name registration
storage_init(X) ->
    global:register_name(X, self()),
    storage([]).

%Function for receiving numbers and storing them in a list
%Sends the list to the scheduler when prompted
storage(List) ->
    receive 
        X when is_integer(X) ->
            storage(List++[X]);
        get_stored ->
            Scheduler = get_pid(global:whereis_name(scheduler), scheduler@asus, scheduler),
            Scheduler!{self(), List},
            storage(List);
        stop ->
            init:stop()
    end.

%Function for calculating if a number is prime
is_prime(X) when X =< 3 -> X > 1;
is_prime(X) when X rem 2 == 0 -> false;
is_prime(X) when X rem 3 == 0 -> false;
is_prime(X) -> is_prime(X, 4).
is_prime(X, I) when X rem I == 0 ->
    false;
is_prime(X, I) ->
    Pow = pow(I, 2),
    if Pow < X -> is_prime(X, I + 2);
       true -> true
    end.

%Sends a number to a storage node based on it's primality
store_number(X, true) ->
    S_prime = get_pid(global:whereis_name(storage_prime), storage_prime@asus, storage_prime),
    S_prime!X;
store_number(X, false) ->
    S_composite = get_pid(global:whereis_name(storage_composite), storage_composite@asus, storage_composite),
    S_composite!X.

%Worker initialization and name registration
worker_init(X) ->
    global:register_name(X, self()),
    worker().

%Function waits for a number and stores it on a storage node
%Returns the scheduler the timestamp when it was done with the job
worker() ->
    receive
        X when is_integer(X) ->
            Condition = is_prime(X),
            store_number(X, Condition),
            Scheduler = get_pid(global:whereis_name(scheduler), scheduler@asus, scheduler),
            Scheduler!{self(), erlang:system_time()},
            worker();
        stop ->
            init:stop()
    end.

%Sends the number to a worker based on the time the workers were busy
%Resets the counter if it comes to a integer overflow
round_robin([T0, T1], X) when (T0 < 0) or (T1 < 0) ->
    round_robin([0,0], X);
round_robin([T0, T1], X) when T0 =< T1 ->
    W1 = get_pid(global:whereis_name(worker_1), worker_1@asus, worker_1),
    W1!X,
    [T0 - erlang:system_time(), T1];
round_robin([T0, T1], X) when T0 > T1 ->
    W2 = get_pid(global:whereis_name(worker_2), worker_2@asus, worker_2),
    W2!X,
    [T0, T1 - erlang:system_time()].

%Scheduler initialization and name registration
scheduler_init() ->
    global:register_name(scheduler, self()),
    scheduler([0,0]).

%Function waits for a number or command
scheduler(T) ->
    W1 = get_pid(global:whereis_name(worker_1), worker_1@asus, worker_1),
    W2 = get_pid(global:whereis_name(worker_2), worker_2@asus, worker_2),
    S_prime = get_pid(global:whereis_name(storage_prime), storage_prime@asus, storage_prime),
    S_composite = get_pid(global:whereis_name(storage_composite), storage_composite@asus, storage_composite),

    receive
        X when is_integer(X)->
            T_adjusted = round_robin(T, X),
            scheduler(T_adjusted); 
        {W1, T_worker} ->
            [T0, T1] = T,
            scheduler([T0 + T_worker, T1]);
        {W2, T_worker} ->
            [T0, T1] = T,
            scheduler([T0, T1 + T_worker]);
        {S_composite, X} ->
            io:format("Composite numbers: ~w~n", [X]),
            scheduler(T);
        {S_prime, X} ->
            io:format("Prime numbers: ~w~n", [X]),
            scheduler(T);
        get_prime ->
            S_prime!get_stored,
            scheduler(T);
        get_composite ->
            S_composite!get_stored,
            scheduler(T);
        stop ->
            W1!stop,
            W2!stop,
            S_composite!stop,
            S_prime!stop,
            init:stop()
        end.

%Function for getting the PID of a process on a distributed node
get_pid(undefined, Node, Name) ->
    net_kernel:connect_node(Node),
    global:sync(),
    global:whereis_name(Name);
get_pid(Pid, _, _) ->
    Pid.

%Initialization of nodes and starting their processes
start_system() ->
    spawn('storage_prime@asus', dz, storage_init, [storage_prime]),
    spawn('storage_composite@asus', dz, storage_init, [storage_composite]),
    spawn('worker_1@asus', dz, worker_init, [worker_1]),
    spawn('worker_2@asus', dz, worker_init, [worker_2]),
    spawn('scheduler@asus', dz, scheduler_init, []).



