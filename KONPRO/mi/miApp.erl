-module(miApp).
-behaviour(application).

-export([start/2, stop/1]).

start(_StartType, _StartArgs) ->
    case mi_sup:start_link() of
        {ok, Pid} ->
            {ok, Pid};
        Error ->
            Error
    end.

stop(_State) ->
    ok.
