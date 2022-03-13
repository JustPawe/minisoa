# MiniProject SOA

The MiniProject SOA toolkit includes a generic `Orchestrator`, and tools for creating local services via Docker. The `Orchestrator` can be used to run a local SOA program with remote services as well.

## Installation

_Requires python3, docker and docker-compose_

### Installing Docker for Ubuntu

You'll want to install `Docker Engine` first: [Docker Engine](https://docs.docker.com/engine/install/ubuntu/).
The installation docs are pretty clear. I would recommend the `Install using the repository` method.

Then you'll want to install `Docker-Compose`: [Docker Compose](https://docs.docker.com/compose/install/).

After that, to avoid having to do `sudo` with every docker command I would follow these steps:
[Optional post-install steps](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).

---

## Setup

**Download the code as ZIP**

[Download here](https://github.com/JustPawe/minisoa/archive/refs/heads/main.zip)

After downloading, extract a zip to your preffered location, which will be the SOA project root directory.


### Running commands

Commands are executed against the docker containers via `./minisoa`

Available commands are `start`, `stop`, `check` and `new`

To get a full list of commands please use the `--help` option on the `./minisoa` script.

```bash
# e.g checking if docker and docker-compose are installed correctly
./minisoa check

# e.g creating a new service
./minisoa new
```

## Docs
- **For the XML Schema documentation** [click here](documentation/xmlinfo.md)
- **For the generic information about the Services** [click here](documentation/service.md)

## Contact

For any questions please open an Issue.
