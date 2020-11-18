{application, schedulerApp, [
    {description, "Scheduler app"},
    {vsn, "0.0.1"},
    {registered, [schedulerApp, scheduler_sup, scheduler]},
    {applications, [kernel, stdlib]},
    {mod, {schedulerApp, []}},
    {env, []}
    ]}.
