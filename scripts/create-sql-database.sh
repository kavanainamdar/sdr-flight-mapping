#!/bin/bash

# Before running this script, ensure you have the Azure CLI installed and configured
# Use EXPORT to set the environment variable for the database password
# For example:
# export FLIGHTDB_PASSWORD="xxxxxxxxxx"


az login 

# Create a resource group
# Replace 'westus2' with your preferred Azure region
# Replace 'sdr-flight-mapping' with your desired resource group name
# Ensure the resource group name is unique across Azure
# and follows Azure naming conventions
az group create --name sdr-flight-mapping --location westus2

# Create an Azure SQL Server
# Replace 'sdr-flight-mapping-sql' with your desired server name
# Ensure the server name is unique across Azure
# Replace 'flighttracker' with your desired admin username
# Replace ${FLIGHTDB_PASSWORD} with your actual password or use an environment variable
# Ensure the password meets Azure SQL Server requirements
az sql server create --name sdr-flight-mapping-sql \
--resource-group sdr-flight-mapping --location westus2 \
--admin-user flighttracker --admin-password ${FLIGHTDB_PASSWORD}

# Create an Azure SQL Database
# Replace 'flightdata' with your desired database name
# The service objective 'Free' is used for development and testing purposes
# For production, consider using a different service objective
az sql db create --resource-group sdr-flight-mapping \
--server sdr-flight-mapping-sql --name flightdata --service-objective Free

# Get your public IP address
MY_IP=$(curl -s https://api.ipify.org)

# Create a firewall rule to allow your IP
az sql server firewall-rule create \
  --resource-group sdr-flight-mapping \
  --server sdr-flight-mapping-sql \
  --name AllowMyIP \
  --start-ip-address $MY_IP \
  --end-ip-address $MY_IP

 # open connection for all azure services
az sql server firewall-rule create \
  --resource-group sdr-flight-mapping \
  --server sdr-flight-mapping-sql \
  --name AllowAllAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0

# create a table to hold flight data
sqlcmd -S sdr-flight-mapping-sql.database.windows.net -d flightdata \
-U flighttracker -P "${FLIGHTDB_PASSWORD}" -i "create-AdsbAircraftData-Table.sql"
