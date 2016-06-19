#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
requires boto3
  install with: sudo pip install boto3

requires configured aws cli:
  aws configure
"""

from __future__ import unicode_literals
from __future__ import print_function

from _version import __version__
from _name import __appname__
__author__ = "Johannes Reichard <mail@johannesreichard.de>"
__license__ = "MIT"


import sys
import argparse
import ConfigParser
import os
from os.path import expanduser, isfile, dirname, exists

import boto3

# available commands
COMMAND_DELETE = 'delete'
COMMAND_RESTORE = 'restore'

# config path relative to home with leading slash
CONFIG_PATH = '%s/.rds-snapshot-restore/config' % expanduser('~')

INSTANCE_IDENTIFIER = 'db_identifier_instance'
INSTANCE_CLASS = 'db_instance_class'
IDENTIFIER_FILTER = 'db_identifier_filter'
AUTOMATED_ONLY = 'automated_only'

CONFIG_DEFAULTS = {
    INSTANCE_IDENTIFIER: 'test-db-automatic',
    INSTANCE_CLASS: 'db.t2.medium',
    IDENTIFIER_FILTER: '',
    AUTOMATED_ONLY: True,
}


def _get_most_current_snapshot():
    """
    finding most current snapshota
    return: (string) DBSnapshotInstance
    """
    rds_client = boto3.client('rds')
    identifier_filter = config.get('DEFAULT', IDENTIFIER_FILTER)
    automated_only = config.getboolean('DEFAULT', AUTOMATED_ONLY)
    snapshot_type = 'automated' if automated_only else None

    # get snapshot description from rds client
    snapshots = rds_client\
        .describe_db_snapshots(SnapshotType=snapshot_type)['DBSnapshots']

    if identifier_filter and not 'None':
        snapshots = filter(lambda x: identifier_filter in
                           x.get('DBInstanceIdentifier'), snapshots)

    # sort descending and retrieve most current entry
    try:
        most_current_snapshot = sorted(
            snapshots,
            cmp=lambda x, y: cmp(x.get('SnapshotCreateTime'),
                                 y.get('SnapshotCreateTime')),
            reverse=True)[0]
    except IndexError:
        raise StandardError('could not find a snapshot')

    # result
    identifier = most_current_snapshot.get('DBSnapshotIdentifier')

    if identifier:
        return identifier
    else:
        raise StandardError(
            'could not determin most current snapshot with filter %s'
            % DB_IDENTIFIER_FILTER)


def _read_config():
    """
    get config
    if no default config existing also writes default config to file
    """
    global config
    config = ConfigParser.SafeConfigParser(CONFIG_DEFAULTS)

    # add config dir if not existing
    directory = dirname(CONFIG_PATH)

    if not exists(directory):
        os.makedirs(directory)

    # write default config if not existing
    if (not isfile(CONFIG_PATH)):
        # write default config if not existing
        config.write(open(CONFIG_PATH, 'w'))

    config.read(CONFIG_PATH)


def restore_instance(db, snapshot, instance_class=None):
    """given snapshot to configured db instance name"""
    if not instance_class:
        instance_class = config.get('DEFAULT', INSTANCE_CLASS)

    sys.stdout.write(
        'Restore snapshot %s to instance %s, confirm with YES (all capitals)\n'
        % (snapshot, db))
    choice = raw_input()

    if choice == 'YES':
        print('Restoring %s to %s' % (snapshot, db))

        rds_client = boto3.client('rds')
        rds_client.restore_db_instance_from_db_snapshot(
            DBInstanceIdentifier=db,
            DBSnapshotIdentifier=snapshot,
            DBInstanceClass=instance_class,
        )


def delete_instance(db):
    """prompting for confirmation -> delete configured db instance"""

    sys.stdout.write('Confirm deletion of %s with YES (all capitals)\n' % db)
    choice = raw_input()

    if choice == 'YES':
        print('Deleteing instance %s' % db)
        rds_client = boto3.client('rds')

        rds_client.delete_db_instance(
            DBInstanceIdentifier=db,
            SkipFinalSnapshot=True
        )
    else:
        print('exit')
        exit


def main():
    parser = argparse.ArgumentParser()
    _read_config()

    # add args
    parser.add_argument('command',
                        type=str,
                        choices=[COMMAND_RESTORE, COMMAND_DELETE])
    parser.add_argument('--db-identifier',
                        help='db_instance_identifier (maschine name)',
                        type=str)

    # parse args
    args = parser.parse_args()
    command = args.command

    if args.db_identifier:
        db_identifier = args.db_identifier
    else:
        db_identifier = config.get('DEFAULT', INSTANCE_IDENTIFIER)

    # execute commands
    if command == COMMAND_RESTORE:
        # create / restore snapshot to instance
        snapshot_identifier = _get_most_current_snapshot()
        restore_instance(db_identifier, snapshot_identifier)
    elif command == COMMAND_DELETE:
        # delete instance
        delete_instance(db_identifier)


if __name__ == '__main__':
    main()
