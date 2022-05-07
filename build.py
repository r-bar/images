#!/usr/bin/env python3

import os
from argparse import ArgumentParser
from pathlib import Path
from subprocess import run

CONTAINER_REGISTRY = os.environ.get("CONTAINER_REGISTRY", "registry.barth.tech/library")
CONTAINER_RUNTIME = os.environ.get("CONTAINER_RUNTIME", "podman")


class Cli(ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_argument("command")
        self.add_argument("project", nargs='?')
        self.add_argument("tag", nargs='?')
        self.add_argument("--dry-run", action="store_true")
        self.args = self.parse_args()


def build(project, tag, dry_run=False):
    project_dir = Path("images") / project
    dockerfile = project_dir / "Dockerfile"
    tagfile = project_dir / "tags" / tag
    context = project_dir / "files"
    command = [
        CONTAINER_RUNTIME,
        "build",
        str(context),
        "-f",
        str(dockerfile),
        "-t",
        f"{CONTAINER_REGISTRY}/{project}:{tag}",
    ]
    with open(tagfile) as f:
        for line in f:
            command += [arg for arg in line.split() if arg]
    print(*command)
    if not dry_run:
        run(command, check=True)


def build_all(dry_run=False):
    for path in Path('images').glob("*/tags/*"):
        project = path.parts[1]
        tag = path.parts[3]
        build(project, tag, dry_run)


def push(project, tag, dry_run=False):
    image = f"{CONTAINER_REGISTRY}/{project}:{tag}"
    command = [CONTAINER_RUNTIME, 'push', image]
    print(*command)
    if not dry_run:
        run(command, check=True)


def push_all(dry_run=False):
    for path in Path('images').glob("*/tags/*"):
        project = path.parts[1]
        tag = path.parts[3]
        push(project, tag, dry_run)


def main():
    cli = Cli()
    match cli.args.command:
        case "build":
            build(cli.args.project, cli.args.tag, cli.args.dry_run)
        case "build-all":
            build_all(cli.args.dry_run)
        case "push":
            push(cli.args.project, cli.args.tag, cli.args.dry_run)
        case "push-all":
            push_all(cli.args.dry_run)
        case _:
            print(f"Unknown command {cli.args.command}")
            cli.print_help()


if __name__ == "__main__":
    main()
