-module(worker).
-behaviour(gen_server).
-export([start_link/1]).

-export([init/1, handle_call/3, handle_cast/2, handle_info/2, terminate/2, code_change/3]).


start_link(Name) ->
    gen_server:start_link({global, Name}, ?MODULE, Name, []).

init(Name) ->
    {ok, Name}.
handle_call(_, _, Name) ->
    {stop, normal, stopped, Name}.

handle_cast({add, X}, Name) ->
    Condition = is_prime(X),
    store_number(X, Condition),
    Time = erlang:system_time(),
    gen_server:cast(scheduler, {Name, Time}),
    {noreply, Name}.

handle_info(_Info, State) ->
    {noreply, State}.
terminate(_Reason, _State) ->
    ok.
code_change(_OldVsn, State, _Extra) ->
    {ok, State}.

sync(Node) ->
    net_kernel:connect_node(Node),
    global:sync().

%Function for calculating if a number is prime
is_prime(X) when X =< 3 -> X > 1;
is_prime(X) when X rem 2 == 0 -> false;
is_prime(X) when X rem 3 == 0 -> false;
is_prime(X) -> is_prime(X, 4).
is_prime(X, I) when X rem I == 0 ->
    false;
is_prime(X, I) ->
    Pow = math:pow(I, 2),
    if Pow < X -> is_prime(X, I + 2);
       true -> true
    end.

%Sends a number to a storage node based on it's primality
store_number(X, true) ->
    sync(storage_prime@asus),
    gen_server:cast(storage_prime, X);
store_number(X, false) ->
    sync(storage_composite@asus),
    gen_server:cast(storage_composite, X).

