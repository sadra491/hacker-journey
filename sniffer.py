import socket
import struct

def sniff_packets():
    # ساخت یک سوکت خام برای شنود پکت‌های شبکه
    try:
        conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    except PermissionError:
        print("[-] Error: You need root privileges to run this script.")
        return

    print("[*] Starting packet sniffer... (Press Ctrl+C to stop)")
    
    while True:
        raw_data, addr = conn.recvfrom(65535)
        
        # پارس کردن هدر اترنت (۱۴ بایت اول)
        eth_header = raw_data[:14]
        eth = struct.unpack('!6s6sH', eth_header)
        eth_protocol = socket.ntohs(eth[2])
        
        # اگر پروتکل IP بود (0x0800)
        if eth_protocol == 8:
            # پارس کردن هدر IP (۲۰ بایت بعدی)
            ip_header = raw_data[14:34]
            iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
            version_ihl = iph[0]
            version = version_ihl >> 4
            ihl = version_ihl & 0xF
            iph_length = ihl * 4
            
            src_ip = socket.inet_ntoa(iph[8])
            dst_ip = socket.inet_ntoa(iph[9])
            protocol = iph[6]
            
            print(f"IP Packet: {src_ip} -> {dst_ip} | Protocol: {protocol}")

if __name__ == "__main__":
    sniff_packets()
