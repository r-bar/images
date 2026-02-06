#!/usr/bin/env python3

import itertools as it
import json
import os
import sys
import tomllib
from dataclasses import dataclass, field, asdict
from argparse import ArgumentParser
from pathlib import Path
from subprocess import run
from typing import Iterable, Literal, ClassVar

PROJECT = "library"
CONTAINER_REGISTRY = os.environ.get("CONTAINER_REGISTRY", "registry.barth.tech")
CONTAINER_RUNTIME = os.environ.get("CONTAINER_RUNTIME", "podman")
GIT_ROOT = Path(__file__).parent
IMAGE_DIRECTORY = GIT_ROOT / "images"
TAG_FILE = "tags.toml"


@dataclass(frozen=True, kw_only=True)
class Image:
    name: str
    full_name: str
    tag: str
    repository: str
    build_args: dict[str, str] = field(default_factory=dict)
    dockerfile: str
    imageDir: str
    context: str
    registry: str
    project: str


@dataclass(frozen=True, kw_only=True)
class TagData:
    """Structure for each entry in a tags.toml file"""
    tag: str
    dockerfile: str = "Dockerfile"
    args: dict[str, str] = field(default_factory=dict)

    @classmethod
    def load(cls, file: Path | str) -> list["TagData"]:
        tags = []
        with open(file, "rb") as f:
            data = tomllib.load(f)
        for tag, config in data.items():
            tags.append(cls(tag=tag, **config))
        return tags


class Cli:
    """Management script for building and pushing images in this repository."""

    command: Literal["build", "push", "images"]
    image: str | None
    tag: str | None
    dry_run: bool
    extra_args: list[str]
    parser: ArgumentParser

    def __init__(self, *args, argv=sys.argv[1:], **kwargs):
        self.parser = parser = ArgumentParser(description=self.__doc__)
        sub = parser.add_subparsers(dest="command")

        _images = sub.add_parser("images", help="List images and tags")

        build = sub.add_parser("build", help="Build images")
        build.add_argument("image", nargs="?")
        build.add_argument("tag", nargs="?")
        build.add_argument("--dry-run", action="store_true")

        push = sub.add_parser("push", help="Push images")
        push.add_argument("--image", nargs="?")
        push.add_argument("--tag", nargs="?")
        push.add_argument("--dry-run", action="store_true")

        args, self.extra_args = parser.parse_known_args()
        for k, v in vars(args).items():
            setattr(self, k, v)


def images(
    image_filter: str | None = None, tag_filter: str | None = None
) -> Iterable[Image]:
    # print('image directory:', IMAGE_DIRECTORY, file=sys.stderr)
    assert IMAGE_DIRECTORY.is_dir()
    for image_dir in IMAGE_DIRECTORY.iterdir():
        if image_dir.name.startswith("_") or image_filter and image_dir.name != image_filter:
            continue
        rel_image_dir = image_dir.relative_to(GIT_ROOT)
        repository = f"{CONTAINER_REGISTRY}/{PROJECT}/{image_dir.name}"
        tag_file = image_dir / TAG_FILE
        tags = TagData.load(tag_file)
        for config in tags:
            if tag_filter and config.tag != tag_filter:
                continue
            yield Image(
                full_name=f"{repository}:{tag_file.name}",
                name=image_dir.name,
                tag=config.tag,
                repository=repository,
                registry=CONTAINER_REGISTRY,
                project=PROJECT,
                build_args=config.args,
                dockerfile=str(rel_image_dir / config.dockerfile),
                imageDir=str(rel_image_dir),
                context=str(rel_image_dir / "files"),
            )


def run_build(image: Image, dry_run: bool = False, extra_args: list[str] | None = None):
    """Run the image build command"""
    extra_args = extra_args or []
    command = [
        CONTAINER_RUNTIME,
        "build",
        image.context,
        "-f",
        image.dockerfile,
        "-t",
        image.full_name,
    ]
    command += list(
        it.chain.from_iterable(
            ("--build-arg", f"{k}={v}") for k, v in image.build_args.items()
        )
    )
    print(*command)
    if not dry_run:
        run(command, check=True)


def build(
    image_filter: str | None,
    tag_filter: str | None,
    dry_run: bool = False,
    extra_args: list[str] | None = None,
):
    """Build all specified images. Translate cli arguments into """
    for image in images(image_filter, tag_filter):
        run_build(image, dry_run, extra_args)


def run_push(image: Image, dry_run: bool = False, extra_args: list[str] | None = None):
    """Run the image push command"""
    extra_args = extra_args or []
    command = [CONTAINER_RUNTIME, "push", image.full_name]
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
    match cli.command:
        case "build":
            build(cli.image, cli.tag, cli.dry_run, cli.extra_args)
        case "push":
            push(cli.image, cli.tag, cli.dry_run, cli.extra_args)
        case "images":
            image_data = [asdict(i) for i in images(cli.image, cli.tag)]
            json.dump(image_data, sys.stdout, indent=2)
        case _:
            print(f"Unknown command {cli.command}")
            cli.print_help()
            exit(1)


if __name__ == "__main__":
    main()
