# rds_snapshot_restore
Restoring and deleting snapshots to new rds instance for ad hoc development db
with (nearly) live data

Picks automatically the most recent snapshot from specified rds-instance to 
restore this snapshot to a new instance. Either choose name on execution or configure
for easier access.
When done with work, easily delete the rds-instance again with one command.

To prevent errors the tool prompts before every execution for confirmation!

## Requirements

- boto3 https://github.com/boto/boto3
- configured aws cli https://aws.amazon.com/cli/

## Configuration

Configuration lies in `~/.rds_shapshoot_restore/config` and looks like the following
snippet (defaults):

    [DEFAULT]
    db_instance_class = db.t2.medium
    db_identifier_instance = test-db-automated
    db_identifier_filter = None
    automated_only = True

Meaning:
- `db_instance_class` instance class for the new rds instance to restore to, see
    [https://docs.aws.amazon.com//cli/latest/reference/rds/restore-db-instance-from-db-snapshot.html#options]
- `db_identifier_instance` name of the instance
- `db_identifier_filter` filter for snapshots of instances (optional)
- `automated_only` filter for automated snapshots only


## Disclaimer

This tool is for development purposes and only manually tested. I do not take
responsibility for ANY errors when using this tool.

This tool normaly works in close perimeter of your live data, I encurage you to read
the source to assess the risk for your usecase.

