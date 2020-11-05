-module(server).
-export([start/1]).

sum_list([]) -> 0;
sum_list([H|T]) -> 
    H + sum_list(T).

min_compare(X, Y) when X =< Y -> X;
min_compare(X, Y) when X > Y -> Y.

minimum([]) -> [];
minimum([H|T]) ->
    min_compare(H, minimum(T)).

max_compare(X, Y) when X =< Y -> Y;
max_compare(X, Y) when X > Y -> X.

maximum([]) -> 0;
maximum([H|T]) ->
    max_compare(H, maximum(T)).

divisible([], _) -> [];
divisible([H|T], N) when H rem N == 0 -> [H|divisible(T, N)];
divisible([H|T], N) when H rem N =/= 0 -> divisible(T,N).

listen(List, Msg) ->
    receive
        N when is_number(N) ->
            L = divisible(List, N),
            io:format("~p\n",[L]),
            listen(List, Msg);
        N when is_list(N) -> 
            io:format("~p\n", [Msg]),
            listen(List, N);
        zbroj ->
            Sum = sum_list(List),
            io:format("~p\n",[Sum]),
            listen(List, Msg);
        najmanji ->
            Min = minimum(List),
            io:format("~p\n", [Min]),
            listen(List, Msg);
        najveci ->
            Max = maximum(List),
            io:format("~p\n", [Max]),
            listen(List, Msg);
        {kloniraj, L2} ->
            Pid = start(L2),
            io:format("~p\n", [Pid]),
            listen(List, Msg);
        _ ->
            io:format("~p\n", ["Error"]),
            listen(List, Msg)
    end.

start(List) ->
   spawn(fun() -> listen(List, "") end).


