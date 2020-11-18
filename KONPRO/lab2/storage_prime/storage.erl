-module(storage).
-behaviour(gen_server).
-export([start_link/1]).

-export([init/1, handle_call/3, handle_cast/2, handle_info/2, terminate/2, code_change/3]).


start_link(Name) ->
    gen_server:start_link({global, Name}, ?MODULE, [], []).

init([]) ->
    {ok, []}.

handle_call(get, _From, State) ->
    {reply, State, State}.

handle_cast(X, State) ->
    NewState = State++[X],
    {noreply, NewState}.



handle_info(_Info, State) ->
    {noreply, State}.
terminate(_Reason, _State) ->
    ok.
code_change(_OldVsn, State, _Extra) ->
    {ok, State}.
