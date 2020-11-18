{application, workerApp, [
    {description, "Worker app"},
    {vsn, "0.0.1"},
    {registered, [workerApp, worker_supp, worker_2]},
    {applications, [kernel, stdlib]},
    {mod, {workerApp, [worker_2]}},
    {env, []}
    ]}.
