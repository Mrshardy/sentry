from django import VERSION
from django.db import models

from sentry.new_migrations.monkey.executor import SentryMigrationExecutor
from sentry.new_migrations.monkey.fields import deconstruct

LAST_VERIFIED_DJANGO_VERSION = (3, 2)
CHECK_MESSAGE = """Looks like you're trying to upgrade Django! Since we monkeypatch
the Django migration library in several places, please verify that we have the latest
code, and that the monkeypatching still works as expected. Currently the main things
to check are:
 - `django.db.migrations.executor.MigrationExecutor`. The `is_dangerous` flag should
   continue to work here when we set `MIGRATION_SKIP_DANGEROUS=1` as an environment
   variable. Confirm that the structure of the class hasn't drastically changed.
- `django.db.migrations.writer.MIGRATION_TEMPLATE`. Verify that the template hasn't
  significantly changed. Details on what we've changed are in a comment on
  `sentry.migrations.monkey.writer.SENTRY_MIGRATION_TEMPLATE`

When you're happy that these changes are good to go, update
`LAST_VERIFIED_DJANGO_VERSION` to the version of Django you're upgrading to. If the
changes are backwards incompatible, change the monkeying to handle both versions.
"""

if VERSION[:2] > LAST_VERIFIED_DJANGO_VERSION:
    raise Exception(CHECK_MESSAGE)


# This should be exactly the same as MIGRATION_TEMPLATE in `django.db.migrations.writer.py`,
# except that we add our own `is_dangerous = False` to the class definition,
# and set django's `atomic = True`.
# Compare this template after each Django version bump to make
# sure we're not missing any important changes.
SENTRY_MIGRATION_TEMPLATE = """\
%(imports)s
from sentry.new_migrations.migrations import CheckedMigration


class Migration(CheckedMigration):
    # This flag is used to mark that a migration shouldn't be automatically run in production. For
    # the most part, this should only be used for operations where it's safe to run the migration
    # after your code has deployed. So this should not be used for most operations that alter the
    # schema of a table.
    # Here are some things that make sense to mark as dangerous:
    # - Large data migrations. Typically we want these to be run manually by ops so that they can
    #   be monitored and not block the deploy for a long period of time while they run.
    # - Adding indexes to large tables. Since this can take a long time, we'd generally prefer to
    #   have ops run this and not block the deploy. Note that while adding an index is a schema
    #   change, it's completely safe to run the operation after the code has deployed.
    is_dangerous = False

    # This flag is used to decide whether to run this migration in a transaction or not. Generally
    # we don't want to run in a transaction here, since for long running operations like data
    # back-fills this results in us locking an increasing number of rows until we finally commit.
    atomic = False

%(replaces_str)s%(initial_str)s
    dependencies = [
%(dependencies)s\
    ]

    operations = [
%(operations)s\
    ]
"""

if VERSION[:2] < (2, 2):
    SENTRY_MIGRATION_TEMPLATE = f"""\
# Generated by Django %(version)s on %(timestamp)s

{SENTRY_MIGRATION_TEMPLATE}
"""
else:
    SENTRY_MIGRATION_TEMPLATE = f"""\
%(migration_header)s{SENTRY_MIGRATION_TEMPLATE}
"""


def monkey_migrations():
    # This import needs to be below the other imports for `executor` and `writer` so
    # that we can successfully monkeypatch them.
    from django.db.migrations import executor, migration, writer

    # monkeypatch Django's migration executor and template.
    executor.MigrationExecutor = SentryMigrationExecutor
    migration.Migration.initial = None
    writer.MIGRATION_TEMPLATE = SENTRY_MIGRATION_TEMPLATE
    models.Field.deconstruct = deconstruct
