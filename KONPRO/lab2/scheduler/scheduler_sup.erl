-module(scheduler_sup).
-behaviour(supervisor).

-export([start_link/0]).

-export([init/1]).
-define(SERVER, ?MODULE).

start_link() ->
    supervisor:start_link({local, ?SERVER}, ?MODULE, []).

init([]) ->
    RestartStrategy = one_for_one,
    MaxRestarts = 3,
    MaxSecondsBetweenRestarts = 10,

    SupFlags = {RestartStrategy, MaxRestarts, MaxSecondsBetweenRestarts},
    Restart = transient,
    Shutdown = 2000,
    Type = worker,
    AChild = {scheduler, {scheduler, start_link, []}, Restart, Shutdown, Type, [scheduler]},
    {ok, {SupFlags, [AChild]}}.

