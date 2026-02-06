# Docker Image Library
A collection of images for common 3rd party applications.


## Building
Build a single image / tag:
```
./build.py build <image> <tag>
```

Build all images
```
./build.py build-all
```

## Pushing
Push a single image / tag:
```
build.py push <image> <tag>
```

Push all images
```
build.py push-all
```

Adding the `--dry-run` argument to any of the above commands will print what
would have been run, but not execute anything.

## Create a new image

Use cookiecutter to template a new repository.

## Repo Structure

Each directory under `/images` represents a seperate image. Each image directory
will contain a `Dockerfile`, a `files` directory that will act as the context
for the build and a `tags` directory.  The tags directory will contain files
named with the tag name and containing any extra build arguments.

Example image directory structure:
```
mumble
├── Dockerfile
├── files
│  └── entrypoint.sh
└── tags
   ├── 1.3.0
   └── latest
```

Example tag file `tags/1.3.0`:
```
-a VERSION=1.3.0
-a TIMEZONE=UTC
```
