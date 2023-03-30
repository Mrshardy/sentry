import click

from sentry.runner.decorators import configuration


@click.group()
def configoptions():
    "Manages Sentry options."


@configoptions.command()
@click.option("--key", "-k", required=True, help="The key of the option to fetch.")
@configuration
def fetch(key):
    "Fetches the option for the given key."
    click.echo(get(key))


@configoptions.command()
@configuration
def list():
    "Fetches all options."
    from sentry import options

    for opt in options.all():
        click.echo(f"{opt.name} ({opt.type}) = {options.get(opt.name)}")


@configoptions.command()
@click.argument("filename", required=True)
@click.option(
    "--dryrun",
    is_flag=True,
    default=False,
    required=False,
    help="Output exactly what changes would be made and in which order.",
)
@configuration
def patch(filename, dryrun):
    "Updates, gets, and deletes options that are each subsectioned in the given file."
    import yaml

    if dryrun:
        click.echo("Dryrun flag on. ")
        with open(filename) as stream:
            data = yaml.safe_load(stream)
            keysToFetch = data["fetch"]
            keysToUpdate = data["update"]
            keysToDelete = data["delete"]

            for key in keysToFetch:
                click.echo(f"Key {key} would be fetched.")

            for key, val in keysToUpdate.items():
                click.echo(f"Would update {key}, {val}.")

            for key in keysToDelete:
                click.echo(f"Would delete {key}.")

    else:
        with open(filename) as stream:
            # todo: add more file validation?
            data = yaml.safe_load(stream)
            keysToFetch = data["fetch"]
            keysToUpdate = data["update"]
            keysToDelete = data["delete"]

            for key in keysToFetch:
                click.echo(get(key))

            for key, val in keysToUpdate.items():
                click.echo(set(key, val))

            for key in keysToDelete:
                click.echo(delete(key))


@configoptions.command()
@click.argument("filename", required=True)
@click.option(
    "--dryrun",
    is_flag=True,
    default=False,
    required=False,
    help="Output exactly what changes would be made and in which order.",
)
@configuration
def strict(filename, dryrun):
    "Deletes everything not in the uploaded file, and applies all of the changes in the file."
    import yaml

    from sentry import options

    if dryrun:
        click.echo("Dryrun flag on. ")

    with open(filename) as stream:
        configmap_data = yaml.safe_load(stream)

        data = configmap_data.get("data", {}).get("options-strict.yaml", "")

        kv_generator = (line.split(": ") for line in data.split("\n") if line)

        db_keys = (opt.name for opt in options.all())

        # update the database to remove all keys NOT in the given file.
        for key in db_keys:
            if key not in kv_generator:
                if dryrun:
                    click.echo(f"Would delete {key}.")
                else:
                    pass
                    # click.echo(delete(key))

        for line in data.split("\n"):
            if line:
                key, val = line.split(": ")
                if dryrun:
                    click.echo(f"Would update {key}, {val}.")
                else:
                    pass
                    # click.echo(set(key, val))


def get(key):
    from sentry import options
    from sentry.options.manager import UnknownOption

    try:
        opt = options.lookup_key(key)
        return f"Fetched Key: {opt.name} ({opt.type}) = {options.get(opt.name)}"
    except UnknownOption:
        return "unknown option: %s" % key


def set(key, val):
    from sentry import options
    from sentry.options.manager import UnknownOption

    try:
        opt = options.lookup_key(key)
        options.set(key, val)
        return f"Updated key: {opt.name} ({opt.type}) = {options.get(opt.name)}"

    except UnknownOption:
        options.register(key)
        options.set(key, val)
        return f"Registered a new key: {key} = {val}"


def delete(key):
    from sentry import options
    from sentry.options.manager import UnknownOption

    try:
        options.lookup_key(key)
        options.delete(key)
        return f"Deleted key: {key}"
    except UnknownOption:
        return "unknown option: %s" % key
