-module(mi).
-behaviour(gen_server).
-export([start_link/0, stop/0, start/1]).

-export([init/1, handle_call/3, handle_cast/2, handle_info/2, terminate/2, code_change/3]).

-define(SERVER, ?MODULE).

%Starts the server
start_link() ->
    gen_server:start_link({local, ?SERVER}, ?MODULE, [], []).

%Stops the process
stop() ->
    gen_server:call(?SERVER, stop).

%Takes a list and calls gen server function call
start(X) ->
    gen_server:call(?SERVER, {start, X}, infinity).

%Initialize the server
init([]) ->
    {ok, []}.

%Stops the server
handle_call(stop, _From, State) ->
    {stop, normal, stopped, State};

%Takes a list from the start function
%Sorts it using external module bucket 
%And calls get_primes to fill the blanks between the sorted number list with primes
handle_call({start, X}, _From, _State) ->
    Sorted = bucket:bucket_sort(X, 5),
    Reply = primes:get_primes(Sorted),
    {reply, Reply, Reply}.

handle_cast(_, State) ->
    {noreply, State}.

handle_info(_Info, State) ->
    {noreply, State}.

terminate(_Reason, _State) ->
    ok.

code_change(_OldVsn, State, _Extra) ->
    {ok, State}.
