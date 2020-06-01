# Docker Image Library
A collection of images for common 3rd party applications.

## Building
```
./build.sh <image_directory>
```

## Repo Structure

Each top level directory represents an image. Each image directory will contain
a Dockerfile and any associated files for building the image. In addition each
image directory will contain a `tags` directory. The tags directory will contain
files named with the tag name and containing any extra build arguments.

Example image directory structure:
```
mumble
├── Dockerfile
├── entrypoint.sh
└── tags
   ├── 1.3.0
   └── latest
```

Example tag file `tags/1.3.0`:
```
-a VERSION=1.3.0
-a TIMEZONE=UTC
```
