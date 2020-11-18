-module(schedulerApp).
-behaviour(application).

-export([start/2, stop/1]).

start(_StartType, _StartArgs) ->
    case scheduler_sup:start_link() of
        {ok, Pid} ->
            {ok, Pid};
        Error ->
            Error
    end.

stop(_State) ->
    ok.
