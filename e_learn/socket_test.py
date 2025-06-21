import socket
try:
    print("Testing IPv6...")
    socket.create_connection(("ipv6.google.com", 80), timeout=5)
    print("IPv6 is working!")
except Exception as e:
    print("IPv6 failed:", e)
