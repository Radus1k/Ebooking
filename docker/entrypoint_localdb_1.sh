# #!/bin/bash


# set -e


# echo "Running tasks...";

# sed -i "s/#\?wal_level = .*/wal_level = replica/" /var/lib/postgresql/data/pgdata/postgresql.conf
# # Update max_connections and shared_buffers in postgresql.conf
# sed -i "s/^#*max_connections = .*/max_connections = 200/" /var/lib/postgresql/data/pgdata/postgresql.conf
# sed -i "s/^#*shared_buffers = .*/shared_buffers = 4GB/" /var/lib/postgresql/data/pgdata/postgresql.conf

# echo "Sid overwrited successfully";

# # Set PostgreSQL environment variables
# export PGDATA="/var/lib/postgresql/data/pgdata"
# # Set PostgreSQL configuration options
# sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/g" "$PGDATA/postgresql.conf"
# echo "max_replication_slots = 10" >> "$PGDATA/postgresql.conf"
# echo "shared_preload_libraries = 'pglogical'" >> "$PGDATA/postgresql.conf"
# echo "wal_level = logical" >> "$PGDATA/postgresql.conf"
# echo "max_wal_senders = 10" >> "$PGDATA/postgresql.conf"
# echo "max_worker_processes = 10" >> "$PGDATA/postgresql.conf"
# echo "max_connections = 500" >> "$PGDATA/postgresql.conf"
# echo "synchronous_commit = off" >> "$PGDATA/postgresql.conf"
# echo "max_standby_streaming_delay = -1" >> "$PGDATA/postgresql.conf"
# echo "hot_standby = on" >> "$PGDATA/postgresql.conf"

# echo "Echo overwrited successfully";



# # Start PostgreSQL
# # exec gosu postgres postgres -D /var/lib/postgresql/data/pgdata \
# #     -c listen_addresses='*' \
# #     -c max_replication_slots=10 \
# #     -c shared_preload_libraries='pglogical' \
# #     -c wal_level=logical \
# #     -c max_wal_senders=10 \
# #     -c max_worker_processes=10 \
# #     -c max_connections=500 \
# #     -c synchronous_commit=off \
# #     -c max_standby_streaming_delay=-1 \
# #     -c hot_standby=on



# # CREATE EXTENSION IF NOT EXISTS pglogical;
# # SELECT pglogical.create_node(node_name := 'local_node', dsn := 'host=localhost port=5432 dbname=local_db1 user=postgres password=postgres');
# # SELECT pglogical.create_subscription(subscription_name := 'hotels_subscription_db2', provider_dsn := 'host=34.175.108.166 port=5432 dbname=hotelsdb user=postgres password=postgres', replication_sets := ARRAY['replication_hotelsdb'], synchronize_structure := true, synchronize_data := true);

# echo "shared_preload_libraries = 'pglogical'" >> /var/lib/postgresql/data/postgresql.conf

# # Start PostgreSQL
# gosu postgres postgres &

# # Wait for PostgreSQL to start
# until psql -c '\q'; do
#   sleep 1
# done

# echo "Postgres host: "
# echo $POSTGRES_HOST

# echo "Postgres db: "
# echo $POSTGRES_DB

# echo "Postgres port: "
# echo $POSTGRES_PORT

export PGPASSWORD=postgres

# # exec /usr/local/bin/docker-entrypoint.sh "$@"

# # until pg_isready -h localhost -p 5432 -U postgres; do
# #   echo "Waiting for database server to start up..."
# #   sleep 1
# # done



# # psql  -c "alter system set shared_preload_libraries = 'pglogical';";
# # connect to db 
# # psql "sslmode=disable dbname=postgres user=postgres password=postgres hostaddr=34.175.108.166"

# # psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DB" -U "$POSTGRES_USER" -c "CREATE ROLE replication WITH REPLICATION LOGIN PASSWORD 'password';"

# echo "Shared preload libraried succeedded!"

# psql  -c "CREATE ROLE replication WITH REPLICATION LOGIN PASSWORD 'postgres'";

# echo "CREATE replicated user role succeedded!"

# psql  -c "GRANT REPLICATION TO postgres;"

# echo "Postgres user role updated succeedded!"

# # Enable pglogical extension
# psql -c "CREATE EXTENSION pglogical;"

# echo "added PGLOGICAL succeedded!"

# # psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DB" -U "$POSTGRES_USER" -c "SELECT pglogical.create_node(node_name := 'local_db1_node', dsn := 'host=localhost port=5432 dbname=local_db1 user=postgres password=postgres password=$PGPASSWORD');";

# if psql -tAc "SELECT EXISTS(SELECT 1 FROM pglogical.node WHERE node_name = 'local_db1_node');" | grep -q "t"; then
#   echo "pglogical node 'local_db1_node' already exists"
# else
#   echo "Creating pglogical node 'local_db1_node'"
#   psql -c "SELECT pglogical.create_node(node_name := 'local_db1_node', dsn := 'host=localhost port=5432 dbname=local_db1 user=postgres password=postgres password=$PGPASSWORD');"
# fi

# # psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DB" -U "$POSTGRES_USER" -c "SELECT pglogical.create_subscription(subscription_name := 'subscription_hotelsdb_subscriber1', provider_dsn := 'host=ENV_VRBL port=5432 dbname=hotelsdb user=postgres', replication_sets := ARRAY['replication_hotelsdb'], synchronize_structure := true, synchronize_data := true, forward_origins := '{}', apply_delay := '0 seconds'::interval, subscriber_node_names := ARRAY['subscriber1']);";

# # Create a node for the local PostgreSQL container

# # Create a subscription to the GCP PostgreSQL instance
# psql -c "SELECT pglogical.create_subscription(subscription_name := 'hotels_subscription_db1', provider_dsn := 'host=ENV_VRBL port=5432 dbname=hotelsdb user=postgres password=postgres', replication_sets := ARRAY['replication_hotelsdb'], synchronize_structure := true, synchronize_data := true);";


# echo "Runned successfully";

# # Stop PostgreSQL
# pg_ctl stop

# # Start PostgreSQL with pglogical enabled
# exec gosu postgres postgres -c config_file=/var/lib/postgresql/data/postgresql.conf -c shared_preload_libraries=pglogical

#!/bin/bash

# start PostgreSQL server
service postgresql start

# wait until PostgreSQL server is up and running
while ! pg_isready -q; do
  echo "Waiting for PostgreSQL server to start..."
  sleep 1
done

psql  -c "alter system set shared_preload_libraries = 'pglogical';";

# restart PostgreSQL server
su -p -c "/etc/init.d/postgresql restart"

# wait until PostgreSQL server is up and running again
while ! pg_isready -q; do
  echo "Waiting for PostgreSQL server to restart..."
  sleep 1
done

psql -c "CREATE EXTENSION pglogical;"

# continue with other commands
echo "PostgreSQL server restarted successfully."
