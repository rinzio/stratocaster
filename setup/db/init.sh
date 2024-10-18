#!/bin/bash
#!/bin/bash

RETRIES=10

until mongosh --eval "db.adminCommand('ping')" >/dev/null 2>&1; do
  echo "Waiting for MongoDB connection..."
  sleep 3
  RETRIES=$((RETRIES-1))
  if [ "$RETRIES" -le 0 ]; then
    echo "MongoDB is still not ready, aborting."
    exit 1
  fi
done


mongosh --eval "db = db.getSiblingDB('$MONGO_DB'); db.users.createIndex({ email: 1 }, { unique: true });"
mongosh --eval "db = db.getSiblingDB('$MONGO_DB'); db.users.createIndex({ prof_id: 1 }, { unique: true });"
