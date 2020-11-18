-module(storageApp).
-behaviour(application).

-export([start/2, stop/1]).

start(_StartType, StartArgs) ->
    case storage_sup:start_link(StartArgs) of
        {ok, Pid} ->
            {ok, Pid};
        Error ->
            Error
    end.

stop(_State) ->
    ok.
