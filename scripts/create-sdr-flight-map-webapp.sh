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
  --name sdr-flight-map-webapp \
  --runtime "NODE:22-lts"

cd ../front-end/sdr-flight-map
# Install dependencies and build the application
npm install
npm run build

cp startup.sh build/startup.sh

cd build

# Zip the application files
zip -r sdr-flight-map.zip .

# Deploy the build folder (replace 'build' with your actual build output folder)
az webapp deploy --resource-group sdr-flight-mapping \
  --name sdr-flight-map-webapp \
  --src-path sdr-flight-map.zip

# Set the startup command for the web app
az webapp config set --resource-group sdr-flight-mapping \
  --name sdr-flight-map-webapp \
  --startup-file "startup.sh"


cd ../../../scripts

# clean up the zip file
rm ../front-end/sdr-flight-map/sdr-flight-map.zip