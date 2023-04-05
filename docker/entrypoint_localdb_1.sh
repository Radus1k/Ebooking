#!/bin/bash

set -e

# Create a new user with limited privileges
useradd -ms /bin/bash postgres_user
chown -R postgres_user:postgres_user /var/lib/postgresql/data

# Start PostgreSQL server as postgres_user
exec gosu postgres_user postgres -D /var/lib/postgresql/data \
    -c listen_addresses='*' \
    -c max_replication_slots=10 \
    -c shared_preload_libraries='pglogical' \
    -c wal_level=logical \
    -c max_wal_senders=10 \
    -c max_worker_processes=10 \
    -c max_connections=500 \
    -c synchronous_commit=off \
    -c max_standby_streaming_delay=-1 \
    -c hot_standby=on

# Wait for PostgreSQL to start
until pg_isready
do
    sleep 1s
done

# Create database if it doesn't exist
if ! gosu postgres psql -lqt | cut -d \| -f 1 | grep -qw hotelsdb; then
    gosu postgres psql -c "CREATE DATABASE hotelsdb;"
fi

# Create schema if it doesn't exist
gosu postgres psql -c "CREATE SCHEMA IF NOT EXISTS hotelsdb;" hotelsdb

# Create replication set on local database
gosu postgres psql -c "SELECT pglogical.create_replication_set('my_replication_set', true, 'public.users');" hotelsdb

# Create subscription to global database on local database
gosu postgres psql -c "SELECT pglogical.create_subscription('my_subscription', 'dbname=hotelsdb host=34.175.108.166 user=postgres password=postgres', '{my_replication_set}');" hotelsdb