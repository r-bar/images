#!/usr/bin/env python3

import itertools as it
import json
import os
import sys
from argparse import ArgumentParser
from pathlib import Path
from subprocess import run
from typing import Iterable, TypedDict

PROJECT = "library"
CONTAINER_REGISTRY = os.environ.get("CONTAINER_REGISTRY", "registry.barth.tech")
CONTAINER_RUNTIME = os.environ.get("CONTAINER_RUNTIME", "podman")
GIT_ROOT = Path(__file__).parent
IMAGE_DIRECTORY = GIT_ROOT / "images"


class Image(TypedDict):
    name: str
    fullName: str
    tag: str
    repository: str
    buildArgs: dict[str, str]
    tagFile: str
    dockerfile: str
    imageDir: str
    context: str
    registry: str
    project: str


class Cli(ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_argument("command")
        self.add_argument("--image")
        self.add_argument("--tag")
        self.add_argument("--dry-run", action="store_true")
        self.args, self.extra_args = self.parse_known_args()


def build_args(tagfile: str | Path) -> dict[str, str]:
    """Read the given tagfile and return a dictionary of the build arguments"""
    args = {}
    with open(tagfile) as f:
        for line in f:
            k, v = line.strip().split("=", maxsplit=1)
            args[k] = v
    return args


def images(
    image_filter: str | None = None, tag_filter: str | None = None
) -> Iterable[Image]:
    # print('image directory:', IMAGE_DIRECTORY, file=sys.stderr)
    assert IMAGE_DIRECTORY.is_dir()
    for image_dir in IMAGE_DIRECTORY.iterdir():
        for tag_file in image_dir.joinpath("tags").iterdir():
            if tag_file.name.startswith("."):
                continue
            if tag_filter and tag_file.name != tag_filter:
                continue
            if image_filter and image_dir.name != image_filter:
                continue
            repository = f"{CONTAINER_REGISTRY}/{PROJECT}/{image_dir.name}"
            rel_image_dir = image_dir.relative_to(GIT_ROOT)
            yield {
                "fullName": f"{repository}:{tag_file.name}",
                "name": image_dir.name,
                "tag": tag_file.name,
                "repository": repository,
                "registry": CONTAINER_REGISTRY,
                "project": PROJECT,
                "buildArgs": build_args(tag_file),
                "tagFile": str(tag_file.relative_to(GIT_ROOT)),
                "dockerfile": str(rel_image_dir / "Dockerfile"),
                "imageDir": str(rel_image_dir),
                "context": str(rel_image_dir / "files"),
            }


def run_build(image: Image, dry_run: bool = False, extra_args: list[str] | None = None):
    """Run the image build command"""
    extra_args = extra_args or []
    command = [
        CONTAINER_RUNTIME,
        "build",
        image["context"],
        "-f",
        image["dockerfile"],
        "-t",
        image["fullName"],
    ]
    command += list(
        it.chain.from_iterable(
            ("--build-arg", f"{k}={v}") for k, v in image["buildArgs"].items()
        )
    )
    print(*command)
    if not dry_run:
        run(command, check=True)


def build(
    image_filter: str,
    tag_filter: str,
    dry_run: bool = False,
    extra_args: list[str] | None = None,
):
    """Build all specified images. Translate cli arguments into """
    for image in images(image_filter, tag_filter):
        run_build(image, dry_run, extra_args)


def run_push(image: Image, dry_run: bool = False, extra_args: list[str] | None = None):
    """Run the image push command"""
    extra_args = extra_args or []
    command = [CONTAINER_RUNTIME, "push", image["fullName"]]
    command += extra_args
    print(*command)
    if not dry_run:
        run(command, check=True)


def push(
    image_filter: str | None = None,
    tag_filter: str | None = None,
    dry_run: bool = False,
    extra_args: list[str] | None = None,
):
    """Push all specified images to the registry"""
    for image in images(image_filter, tag_filter):
        run_push(image, dry_run, extra_args)


def main():
    cli = Cli()
    match cli.args.command:
        case "build":
            build(cli.args.image, cli.args.tag, cli.args.dry_run, cli.extra_args)
        case "push":
            push(cli.args.image, cli.args.tag, cli.args.dry_run, cli.extra_args)
        case "images":
            image_data = list(images(cli.args.image, cli.args.tag))
            json.dump(image_data, sys.stdout, indent=2)
        case _:
            print(f"Unknown command {cli.args.command}")
            cli.print_help()


if __name__ == "__main__":
    main()
