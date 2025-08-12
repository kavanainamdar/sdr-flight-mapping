#!/bin/bash

az login 

# Create a resource group
az group create --name sdr-flight-mapping --location westus2

# Create an Azure App Service plan (if not already created)
az appservice plan create --name sdr-flight-mapping-plan --resource-group sdr-flight-mapping \
  --sku FREE --is-linux

# Create an Azure Web App
az webapp create --resource-group sdr-flight-mapping \
  --plan sdr-flight-mapping-plan \
  --name sdr-flight-mapping-api \
  --runtime "PYTHON|3.12"

az webapp config appsettings set \
  -g sdr-flight-mapping \
  -n sdr-flight-mapping-api \
  --settings FLIGHTDB_PASSWORD="${FLIGHTDB_PASSWORD}"

cd ../flights-api
# Zip the application files
zip -r flights-api.zip .

# Deploy the build folder (replace 'build' with your actual build output folder)
az webapp deploy --resource-group sdr-flight-mapping \
  --name sdr-flight-mapping-api \
  --src-path flights-api.zip

# Set the startup command for the web app
az webapp config set --resource-group sdr-flight-mapping \
  --name sdr-flight-mapping-api \
  --startup-file "startup.sh"


cd ../scripts

# clean up the zip file
rm ../flights-api/flights-api.zip