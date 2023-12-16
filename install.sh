
# expects the repository to be cloned within the homeassistant directory

echo "Copying all files from the cloned repo to the Home Assistant custom_components directory..."

cp --verbose ./custom_components/salusfy/*.* ../custom_components/salusfy

echo "Restart Home Assistant to apply the changes"