# Generated by Django 2.2.24 on 2022-05-06 17:11

from django.db import migrations, models

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

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Replay",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ("replay_id", models.CharField(max_length=80)),
                ("replay_data_type", models.PositiveSmallIntegerField()),
                ("timestamp", models.DateTimeField()),
                ("data", models.TextField()),
            ],
        ),
        migrations.AddIndex(
            model_name="replay",
            index=models.Index(
                fields=["replay_id", "replay_data_type", "timestamp"],
                name="replaystore_replay__fb2261_idx",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="replay",
            unique_together={("replay_id", "replay_data_type", "timestamp")},
        ),
    ]
