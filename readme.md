# Smartwifi

Automatically switch to best known WIFI network


## Install

Requires https://developer.gnome.org/NetworkManager/stable/nmcli.html


    pip3 install git+https://github.com/djaney/smartwifi.git


## Usage

    usage: smartwifi [-h] [--monitor] [--print]
    
    Automatically switch to strongest signal
    
    optional arguments:
      -h, --help     show this help message and exit
      --monitor, -m  Continuously monitor
      --print, -p    Print wifi networks


## Notes

do remove password prompt everytime wifi changes

https://askubuntu.com/questions/244567/remove-sudo-password-when-connecting-to-new-wifi-network