#!/usr/bin/env python3

import json
import os
import sys
from argparse import ArgumentParser
from pathlib import Path
from subprocess import run

PROJECT = "library"
CONTAINER_REGISTRY = os.environ.get("CONTAINER_REGISTRY", "registry.barth.tech")
CONTAINER_RUNTIME = os.environ.get("CONTAINER_RUNTIME", "podman")
GIT_ROOT = Path(__file__).parent
IMAGE_DIRECTORY = GIT_ROOT / "images"


class Cli(ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_argument("command")
        self.add_argument("image", nargs="?")
        self.add_argument("tag", nargs="?")
        self.add_argument("--dry-run", action="store_true")
        self.args = self.parse_args()


def build_args(image: str, tag: str) -> dict[str, str]:
    tagfile = IMAGE_DIRECTORY / image / 'tags' / tag
    args = {}
    with open(tagfile) as f:
        for line in f:
            k, v = line.strip().split("=", maxsplit=1)
            args[k] = v
    return args


def images():
    # print('image directory:', IMAGE_DIRECTORY, file=sys.stderr)
    assert IMAGE_DIRECTORY.is_dir()
    for image_dir in IMAGE_DIRECTORY.iterdir():
        for tag_file in image_dir.joinpath('tags').iterdir():
            if tag_file.name.startswith('.'):
                continue
            tag_args = build_args(image_dir.name, tag_file.name)
            yield {
                "image": image_dir.name,
                "tag": tag_file.name,
                "repository": f"{CONTAINER_REGISTRY}/{PROJECT}/{image_dir.name}",
                "buildArgs": " ".join(
                    f"--build-arg '{k}={v}'" for k, v in tag_args.items()
                ),
            }


def build(image, tag, dry_run=False):
    image_dir = IMAGE_DIRECTORY / image
    dockerfile = image_dir / "Dockerfile"
    tagfile = image_dir / "tags" / tag
    context = image_dir / "files"
    command = [
        CONTAINER_RUNTIME,
        "build",
        str(context),
        "-f",
        str(dockerfile),
        "-t",
        f"{CONTAINER_REGISTRY}/{PROJECT}/{image}:{tag}",
    ]
    with open(tagfile) as f:
        for line in f:
            key, value = line.strip().split("=", maxsplit=1)
            command += ["--build-arg", f"{key}={value}"]
    print(*command)
    if not dry_run:
        run(command, check=True)


def build_all(dry_run=False):
    for path in Path("images").glob("*/tags/*"):
        image = path.parts[1]
        tag = path.parts[3]
        build(image, tag, dry_run)


def push(image, tag, dry_run=False):
    image = f"{CONTAINER_REGISTRY}/{image}:{tag}"
    command = [CONTAINER_RUNTIME, "push", image]
    print(*command)
    if not dry_run:
        run(command, check=True)


def push_all(dry_run=False):
    for path in Path("images").glob("*/tags/*"):
        image = path.parts[1]
        tag = path.parts[3]
        push(image, tag, dry_run)


def main():
    cli = Cli()
    match cli.args.command:
        case "build":
            build(cli.args.image, cli.args.tag, cli.args.dry_run)
        case "build-all":
            build_all(cli.args.dry_run)
        case "push":
            push(cli.args.image, cli.args.tag, cli.args.dry_run)
        case "push-all":
            push_all(cli.args.dry_run)
        case "images":
            json.dump(list(images()), sys.stdout, indent=2)
        case _:
            print(f"Unknown command {cli.args.command}")
            cli.print_help()


if __name__ == "__main__":
    main()
