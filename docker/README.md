# Running the Formlabs Local API within Docker

Example of building and running a [Docker](https://www.docker.com/) container that can run the Windows PreFormServer exectuable and use the Formlabs Local API Python library. The Docker container could be run on a cloud provider like AWS or GCP to build automations and integrations that don't run on your local computer.

Formlabs only provides PreFormServer builds for Windows and MacOS while docker containers are usually based on Linux, so we are using [Wine](https://www.winehq.org/) to run the PreFormServer Windows executable within a Linux-based Docker container.

> [!WARNING]  
> This Dockerfile has not been deployed and used in a production service yet.
> Use it as an example, but assume additional customization and testing is needed.

## Building the Docker Container

Build from the root of the formlabs-api-python repo:
```
docker buildx build \
  --platform linux/amd64 \
  -t formlabs-local-api-app -f docker/Dockerfile .
```

To update the PreFormServer version, either edit the Dockerfile or pass in the updated download URL from the [Formlabs API releases page](https://support.formlabs.com/s/article/Formlabs-API-downloads-and-release-notes?language=en_US)
```
docker buildx build \
  --platform linux/amd64 \
  --build-arg ZIP_PATH=https://downloads.formlabs.com/PreFormServer/Release/3.43.1/PreForm_Server_win_3.43.1_release_releaser_462_70877.zip \
  -t formlabs-local-api-app -f docker/Dockerfile .
```

## Running the Docker Container

Run the [example-app.py](example-app.py) sample Python application using the Formlabs Local API minimal library.
```
docker run --platform linux/amd64 -it --rm docker.io/library/formlabs-local-api-app
```

Run PreFormServer within the container and expose its port for making requests from the host operating system. Mount a volume for passing files back and forth. Note: you'll need to create the tmpvol folder first.
```
docker run --platform linux/amd64 -it --rm \
  -p 44388:44388 \
  -v ${PWD}/tmpvol:/workspace/tmpvol \
  docker.io/library/formlabs-local-api-app \
  wine /workspace/PreFormServer/PreFormServer.exe --port 44388
```

Run interactive container without starting the example Python application:
```
docker run --platform linux/amd64 -it --rm docker.io/library/formlabs-local-api-app /bin/bash
```

## Logs
For debugging, additional PreFormServer logs are at stored at `/home/wineuser/.wine/dosdevices/c:/users/wineuser/AppData/Local/Formlabs/PreFormServer/Logs/log.txt`