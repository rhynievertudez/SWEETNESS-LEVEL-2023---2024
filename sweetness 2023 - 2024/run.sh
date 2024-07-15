# If operating system is Linux:
# if [ "$(uname)" == "Linux" ]; then
#     # Install dependencies
#     sudo apt-get install -y qtbase5-dev
#     sudo apt-get install -y python3-pyqt5
# fi

# pip install -r requirements.txt --verbose --break-system-packages

# Build resources
# pyrcc5 -o resources.py resources.qrc

# Permissions fix on folder if linux
if [ "$(uname)" == "Linux" ]; then
    sudo chmod 0700  /run/user/1000/
fi

# Run the application
cd python/main
python main.py
cd ../..

# Pause 
read -p "Press [Enter] key to continue..."