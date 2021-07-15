import subprocess
import time
"""
Based on https://www.reddit.com/r/linux/comments/bbzm9t/automatically_switch_to_the_strongest_wifi_signal/
"""

STRENGTH_DIFFERENCE_THRESHOLD = 12


def main():
    print("Welcome to smartwifi. Network will automatically switch of stronger wifi is detected")
    while True:
        wifi_list = scan_known_wifi()
        # sort by strength
        wifi_list = sorted(wifi_list, key=lambda x: x['strength'], reverse=True)

        # if current connection is not fastest
        if len(wifi_list) >= 2 and not wifi_list[0]['current']:
            fastest = wifi_list[0]['strength']
            current = list(filter(lambda i: i['current'], wifi_list))[0]['strength']
            difference = int(fastest) - int(current)

            if difference >= STRENGTH_DIFFERENCE_THRESHOLD:
                print("switching to {}".format(wifi_list[1]['name']))
                subprocess.run(
                    ["/usr/bin/nmcli",
                     "device",
                     "wifi",
                     "connect",
                     wifi_list[1]['name']])
        time.sleep(10)





def scan_known_wifi():
    network_scan_info = subprocess.run(
        ["/usr/bin/nmcli",
         "-t",  # tabular format, with : as separator
         "-f",  # choose columns included in result
         "ssid,signal,rate,in-use",
         "dev",
         "wifi",
         "list"],
        stdout=subprocess.PIPE,
        universal_newlines=True)

    known_networks_info = subprocess.run(
        ["/usr/bin/nmcli",
         "-t",
         "-f",
         "name",
         "connection",
         "show"],
        stdout=subprocess.PIPE,
        universal_newlines=True)
    # store the names (=SSID) of each known network in a list
    known_networks = known_networks_info.stdout.splitlines()

    networks = []
    for i in network_scan_info.stdout.splitlines():
        name, strength, speed, current = i.split(":")
        if name not in known_networks:
            continue
        networks.append({
            "name": name,
            "strength": strength,
            "speed": speed,
            "current": current == "*",
        })
    return networks





if __name__ == "__main__":
    main()