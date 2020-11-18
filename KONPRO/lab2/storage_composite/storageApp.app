{application, storageApp, [
    {description, "Storage app"},
    {vsn, "0.0.1"},
    {registered, [storageApp, storage_sup, storage_composite]},
    {applications, [kernel, stdlib]},
    {mod, {storageApp, [storage_composite]}},
    {env, []}
    ]}.
