#!/bin/bash

set -e

# CREATE EXTENSION IF NOT EXISTS pglogical;
# SELECT pglogical.create_node(node_name := 'local_node', dsn := 'host=localhost port=5432 dbname=local_db1 user=postgres password=postgres');
# SELECT pglogical.create_subscription(subscription_name := 'hotels_subscription_db2', provider_dsn := 'host=34.175.108.166 port=5432 dbname=hotelsdb user=postgres password=postgres', replication_sets := ARRAY['replication_hotelsdb'], synchronize_structure := true, synchronize_data := true);


# Wait for the PostgreSQL server to start up
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DB" -U "$POSTGRES_USER"; do
  echo "Waiting for database server to start up..."
  sleep 1
done



psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DB" -U "$POSTGRES_USER" -c "alter system set shared_preload_libraries = 'pglogical';";
# Enable pglogical extension
psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DB" -U "$POSTGRES_USER" -c "CREATE EXTENSION IF NOT EXISTS pglogical;"

# Create a node for the local PostgreSQL container
psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DB" -U "$POSTGRES_USER" -c "SELECT pglogical.create_node(node_name := 'local_node', dsn := 'host=localhost port=5433 dbname=local_db1 user=postgres password=postgres');"


psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DB" -U "$POSTGRES_USER" -c "SELECT pglogical.create_subscription(subscription_name := 'subscription_hotelsdb_subscriber2', provider_dsn := 'host=34.175.108.166 port=5432 dbname=hotelsdb user=postgres', replication_sets := ARRAY['replication_hotelsdb'], synchronize_structure := true, synchronize_data := true, forward_origins := '{}', apply_delay := '0 seconds'::interval, subscriber_node_names := ARRAY['subscriber2'])";
# Create a subscription to the GCP PostgreSQL instance
# psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DB" -U "$POSTGRES_USER" -c "SELECT pglogical.create_subscription(subscription_name := 'hotels_subscription_db2', provider_dsn := 'host=34.175.108.166 port=5432 dbname=hotelsdb user=postgres password=postgres', replication_sets := ARRAY['replication_hotelsdb'], synchronize_structure := true, synchronize_data := true);"

# CREATE EXTENSION IF NOT EXISTS pglogical;
# SELECT pglogical.create_node(node_name := 'local_node', dsn := 'host=localhost port=5433 dbname=local_db1 user=postgres password=postgres');
# SELECT pglogical.create_subscription(subscription_name := 'hotels_subscription_db2', provider_dsn := 'host=34.175.108.166 port=5432 dbname=hotelsdb user=postgres password=postgres', replication_sets := ARRAY['replication_hotelsdb'], synchronize_structure := true, synchronize_data := true);