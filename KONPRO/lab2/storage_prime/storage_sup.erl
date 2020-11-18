-module(storage_sup).
-behaviour(supervisor).

-export([start_link/1]).

-export([init/1]).
-define(SERVER, ?MODULE).

start_link([Name]) ->
    supervisor:start_link({local, ?SERVER}, ?MODULE, [Name]).

init([Name]) ->
    RestartStrategy = one_for_one,
    MaxRestarts = 3,
    MaxSecondsBetweenRestarts = 10,

    SupFlags = {RestartStrategy, MaxRestarts, MaxSecondsBetweenRestarts},
    Restart = transient,
    Shutdown = 2000,
    Type = worker,
    AChild = {storage, {storage, start_link, [Name]}, Restart, Shutdown, Type, [storage]},
    {ok, {SupFlags, [AChild]}}.

