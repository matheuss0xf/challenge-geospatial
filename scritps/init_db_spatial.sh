#!/bin/bash

DB_PATH="locations.db"
SPATIALITE_PATH="/usr/lib/x86_64-linux-gnu/mod_spatialite.so"

echo "Checking for existing SQLite database with SpatiaLite support..."

# Skip creation if database already exists
if [ -f "$DB_PATH" ]; then
    echo "Database '$DB_PATH' already exists. No changes made."
    exit 0
fi

echo "Creating SQLite database with SpatiaLite..."

sqlite3 "$DB_PATH" <<EOF
.load '$SPATIALITE_PATH'
SELECT InitSpatialMetaData();

CREATE TABLE locations (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL
);
SELECT AddGeometryColumn('locations', 'geom', 4326, 'POINT', 'XY');
SELECT CreateSpatialIndex('locations', 'geom');
EOF

echo "Database '$DB_PATH' created with geospatial support and spatial index!"
