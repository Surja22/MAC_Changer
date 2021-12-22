"""
MAC Changer documentation

1.  Stop your lan : ifconfig eth0 down

2.  Set your own MAC : ifconfig eth0 hw ether "your MAC address"

3. Start your lan : ifconfig eth0 up

"""

# !/usr/bin/env python3

import subprocess as sp
import optparse
import re


# print(f"{option} [+] {argument}")


def get_argument():
    parse = optparse.OptionParser()
    # print(parse)
    parse.add_option("-i", "--interface", dest="interface", help="Enter your interface [wlan0/eth0]")
    parse.add_option("-m", "--mac", dest="new_mac",
                     help="Enter new MAC address [aa:bb:cc:dd:ee:ff] for your interface [wlan0/eth0]")
    (options, arguments) = parse.parse_args()
    if not options.interface or not options.new_mac:
        parse.error("[-] Please enter interface and new mac address value or type --help for more information")
    return options


def change_mac(interface, new_mac):
    print(f"[+] Changing new MAC address {new_mac} to {interface} [+]")
    sp.call(["ifconfig", interface, "down"])
    sp.call(["ifconfig", interface, "hw", "ether", new_mac])
    sp.call(["ifconfig", interface, "up"])


#
# interface = option.interface
# new_mac = option.new_mac
#
#
# # sp.call(f"ifconfig {interface} down", shell=True)
# # sp.call(f"ifconfig {interface} hw ether {new_mac}", shell=True)
# # sp.call(f"ifconfig {interface} up", shell=True)
#
# # we should not execute the above code as it allows shell execution. To mitigate shell attack, execute below script.
#
def get_current_mac(interface):
    mac_output = str(sp.check_output(["ifconfig", interface]))
    # print(type(mac_output))
    is_new_mac_change = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", mac_output)
    # print(is_new_mac_change.group(0))
    if is_new_mac_change:
        return is_new_mac_change.group(0)
    else:
        print("[-] Interface has not been found!")


option = get_argument()
current_mac_addr = get_current_mac(option.interface)
# print(current_mac_addr)
if current_mac_addr is not None:
    change_mac(option.interface, option.new_mac)
    new_mac_addr = get_current_mac(option.interface)
    if new_mac_addr == option.new_mac:
        print(f"[+] Script executed successfully! [+]\n[+]New MAC address : {option.new_mac} has been assigned in {option.interface}[+]")
    else:
        print("[-]Script execution failed![-]")

#
