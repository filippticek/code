-module(mi_sup).
-behaviour(supervisor).

-export([start_link/0]).

-export([init/1]).
-define(SERVER, ?MODULE).

start_link() ->
    supervisor:start_link({local, ?SERVER}, ?MODULE, []).

init([]) ->
    RestartStrategy = one_for_one,
    MaxR = 3,
    MaxT = 20,

    SupFlags = {RestartStrategy, MaxR, MaxT},
    Restart = permanent,
    Shutdown = 2000,
    Type = worker,
    AChild = {mi, {mi, start_link, []}, Restart, Shutdown, Type, [mi]},
    {ok, {SupFlags, [AChild]}}.

