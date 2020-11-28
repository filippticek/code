{application, miApp, [
    {description, "Midterm app"},
    {vsn, "0.0.1"},
    {registered, [miApp, mi_sup, mi]},
    {applications, [kernel, stdlib]},
    {mod, {miApp, []}},
    {env, []}
    ]}.
