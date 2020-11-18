-module(scheduler).
-behaviour(gen_server).
-export([start_link/0, stop/0, add/1, find/1]).

-export([init/1, handle_call/3, handle_cast/2, handle_info/2, terminate/2, code_change/3]).

-define(SERVER, ?MODULE).

start_link() ->
    gen_server:start_link({global, ?SERVER}, ?MODULE, [], []).

stop() ->
    gen_server:call(?SERVER, stop).

add(X) ->
    gen_server:cast(?SERVER, {add, X}).

find(Type) ->
    gen_server:call(?SERVER, {find, Type}).

init([]) ->
    {ok, [0,0]}.

handle_call({find, Type}, _From, State) ->
    case Type of
        prime ->
            sync(storage_prime@asus),
            Reply = gen_server:call(storage_prime, get);
        composite ->
            sync(storage_composite@asus),
            Reply = gen_server:call(storage_composite, get)
    end,
    {reply, Reply, State}.

handle_cast({add, X}, State) ->
    NewState = round_robin(State, X),
    {noreply, NewState};

handle_cast({Name, Time}, State) ->
    [T0, T1] = State,
    case Name of
        worker_1 ->
            NewState = [T0 + Time, T1];
        worker_2 ->
            NewState = [T0, T1 + Time]
    end,
    {noreply, NewState}.

handle_info(_Info, State) ->
    {noreply, State}.

terminate(_Reason, _State) ->
    ok.

code_change(_OldVsn, State, _Extra) ->
    {ok, State}.

sync(Node) ->
    net_kernel:connect_node(Node),
    global:sync().

%Sends the number to a worker based on the time the workers were busy
%Resets the counter if it comes to a integer overflow
round_robin([T0, T1], X) when (T0 < 0) or (T1 < 0) ->
    round_robin([0,0], X);
round_robin([T0, T1], X) when T0 =< T1 ->
    sync(worker_1@asus),
    gen_server:cast(worker_1, {add, X}),
    [T0 - erlang:system_time(), T1];
round_robin([T0, T1], X) when T0 > T1 ->
    sync(worker_2@asus),
    gen_server:cast(worker_2, {add, X}),
    [T0, T1 - erlang:system_time()].

