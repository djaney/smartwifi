import subprocess
import time
import argparse
import warnings

"""
Based on https://www.reddit.com/r/linux/comments/bbzm9t/automatically_switch_to_the_strongest_wifi_signal/
"""

STRENGTH_DIFFERENCE_THRESHOLD = 12


def main():
    parser = argparse.ArgumentParser(description='Automatically switch to strongest signal')
    parser.add_argument('--monitor', '-m', action="store_true", default=False, help='Continuously monitor')
    parser.add_argument('--print', '-p', action="store_true", default=False, help='Print wifi networks')

    args = parser.parse_args()
    while True:
        wifi_list = scan_known_wifi()
        # sort by strength
        wifi_list = sorted(wifi_list, key=lambda x: x['predicted_speed'], reverse=True)

        if args.print:
            for w in wifi_list:
                print("Name={name}, Est. Speed={predicted_speed:0.1f} Net. Speed={network_speed:0.1f} {speed_unit}, "
                      "Signal Strength={strength}, "
                      "Connected={current}".format(**w))

        # if current connection is not fastest
        if len(wifi_list) >= 2 and not wifi_list[0]['current']:
            fastest = wifi_list[0]['strength']
            current = list(filter(lambda i: i['current'], wifi_list))

            if len(current) > 0:
                current = current[0]['strength']
                difference = int(fastest) - int(current)

                if difference >= STRENGTH_DIFFERENCE_THRESHOLD:
                    print("switching to {}".format(wifi_list[0]['name']))
                    subprocess.run(
                        ["/usr/bin/nmcli",
                         "device",
                         "wifi",
                         "connect",
                         wifi_list[0]['name']])
        if args.monitor:
            time.sleep(10)
        else:
            break


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
        strength = float(strength)
        speed_unit = ''
        speed_value = 0.0
        try:
            speed_value, speed_unit = speed.split(" ")
            speed_value = float(speed_value)
            predicted_speed = speed_value * (strength / 100)
        except Exception as e:
            predicted_speed = strength
            warnings.warn("unable to parse speed with value {}".format(speed))
        networks.append({
            "name": name,
            "strength": strength,
            "network_speed": speed_value,
            "predicted_speed": predicted_speed,
            "speed_unit": speed_unit,
            "current": current == "*",
        })
    return networks


if __name__ == "__main__":
    main()
