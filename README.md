# haproxy

This is a hack to get `haproxy` into a container using `pack` so it can be deployed on Toolforge.

It is slightly less terrible than the previous solution of dumping the pre-compiled binary onto NFS then executing it in a container.

Once T401075 / T363027 is resolved, this can be replaced.

## Why?

As a workaround for jobs/components not supporting webservices, enabling allow components to be used 'underneath' a proxy.

Once T362077 is done this can be removed.

## Logic
* `project.toml` handles installing the package from upstream
* `setup.py` creates a dummy python package which satisfies poetry
* `entrypoint.py` handles setting up the runtime (config)

## Testing locally
```
$ pack build --builder heroku/builder:24 external-haproxy
```

## Production configuration
Name of the job (kubernetes service) exposing the port:
```
$ toolforge envvars create WEBSERVICE_BACKEND_HOSTNAME cluebotng-reviewer
name                         value
WEBSERVICE_BACKEND_HOSTNAME  cluebotng-reviewer
```

Optionally, the port to connect to:
```
$ toolforge envvars create WEBSERVICE_BACKEND_PORT 8000
name                       value
WEBSERVICE_BACKEND_PORT     8000
```
