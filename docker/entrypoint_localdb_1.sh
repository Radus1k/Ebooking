#!/bin/bash
# set -e


# CREATE EXTENSION IF NOT EXISTS pglogical;
# SELECT pglogical.create_node(node_name := 'local_node', dsn := 'host=localhost port=5432 dbname=local_db1 user=postgres password=postgres');
# SELECT pglogical.create_subscription(subscription_name := 'hotels_subscription_db2', provider_dsn := 'host=34.175.108.166 port=5432 dbname=hotelsdb user=postgres password=postgres', replication_sets := ARRAY['replication_hotelsdb'], synchronize_structure := true, synchronize_data := true);

echo "Postgres host: "
echo $POSTGRES_HOST

echo "Postgres db: "
echo $POSTGRES_DB

echo "Postgres port: "
echo $POSTGRES_PORT

export PGPASSWORD=postgres

# Wait for the PostgreSQL server to start up
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DB" -U "$POSTGRES_USER"; do
  echo "Waiting for database server to start up..."
  sleep 1
done

# connect to db 
# psql "sslmode=disable dbname=postgres user=postgres password=postgres hostaddr=34.175.108.166"

psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DB" -U "$POSTGRES_USER" -c "GRANT REPLICATION TO postgres;"

# Enable pglogical extension
psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DB" -U "$POSTGRES_USER" -c "CREATE EXTENSION IF NOT EXISTS pglogical;"

psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DB" -U "$POSTGRES_USER" -c "SELECT pglogical.create_node(node_name := 'local_db1_node', dsn := 'host=localhost port=5432 dbname=local_db1 user=postgres password=postgres password=$PGPASSWORD');";

# psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DB" -U "$POSTGRES_USER" -c "SELECT pglogical.create_subscription(subscription_name := 'subscription_hotelsdb_subscriber1', provider_dsn := 'host=34.175.108.166 port=5432 dbname=hotelsdb user=postgres', replication_sets := ARRAY['replication_hotelsdb'], synchronize_structure := true, synchronize_data := true, forward_origins := '{}', apply_delay := '0 seconds'::interval, subscriber_node_names := ARRAY['subscriber1']);";

# Create a node for the local PostgreSQL container

# Create a subscription to the GCP PostgreSQL instance
psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DB" -U "$POSTGRES_USER" -c "SELECT pglogical.create_subscription(subscription_name := 'hotels_subscription_db1', provider_dsn := 'host=34.175.108.166 port=5432 dbname=hotelsdb user=postgres password=postgres', replication_sets := ARRAY['replication_hotelsdb'], synchronize_structure := true, synchronize_data := true);";
