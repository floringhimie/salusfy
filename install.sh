#!bin/bash

# expects the repository to be cloned within the homeassistant directory

echo "Copying all files from the cloned repo to the Home Assistant custom_components directory..."

cp --verbose ./salusfy/*.* ../custom_components/salusfy
cp --verbose ./salusfy/simulator/*.* ../custom_components/salusfy/simulator

echo "Restart Home Assistant to apply the changes"