#!/usr/bin bash
echo ""
echo "======================="
echo "Installing Requirements"
echo "======================="
echo ""
sudo apt update -y
sudo apt autoremove -y
sudo apt install python3 -y
pip install logging
pip install socket
pip install ssl
pip install socks
pip install time
echo ""
echo "================"
echo "Install Complete"
echo "================"
echo ""