# SWE40006 Deployment Task 4

Docker images for SWE40006 Deployment Portfolio Task 4.

Target level: Task 4.4 High Distinction

## Contents

| Folder | Level | Application |
|---|---|---|
| task42-flask | 4.2 | Flask web application on port 5000 |
| task43-fastapi | 4.3 | FastAPI web application on port 8000, multi stage build |
| task44-cli | 4.4 | Command line sensor data analyser with a mounted data volume |

## Docker Hub images

```
docker pull <DOCKERHUB-USERNAME>/swe40006-flask:1.0
docker pull <DOCKERHUB-USERNAME>/swe40006-api:1.0
docker pull <DOCKERHUB-USERNAME>/swe40006-analyser:1.0
```

## Build and run

### task42-flask

```
docker build -t swe40006-flask:1.0 .
docker run -d -p 8080:5000 swe40006-flask:1.0
```

Open http://localhost:8080

### task43-fastapi

```
docker build -t swe40006-api:1.0 .
docker run -d -p 8000:8000 -e APP_ENV=production -e OWNER="Jin Shang" swe40006-api:1.0
```

Open http://localhost:8000 and http://localhost:8000/health

### task44-cli

```
docker build -t swe40006-analyser:1.0 .
docker run -v "${PWD}/data:/data" swe40006-analyser:1.0
```

Reads data/readings.csv and writes data/summary.txt on the host.

Override the defaults by passing arguments after the image name:

```
docker run -v "${PWD}/data:/data" swe40006-analyser:1.0 --input /data/readings.csv --output /data/custom.txt
```

## Dockerfile notes

task43-fastapi uses a two stage build. Dependencies are installed in the first
stage and only the installed packages are copied into the runtime image, so the
final image carries no pip cache or build tooling. Both task43 and task44 run as
a non root user. Each folder has a .dockerignore so the build context stays small.
