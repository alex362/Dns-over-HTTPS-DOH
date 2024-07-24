# Dns-over-HTTPS-DOH
This project provides a proof-of-concept implementation of a Command and Control (C2) infrastructure using DNS over HTTPS (DoH). 
DoH C2 allows for covert communication between the C2 server and the infected client machines by leveraging encrypted DNS queries
thereby making the traffic appear legitimate and harder to detect by traditional network monitoring tools.

# Testing and Limitations
This project is intended for educational purposes and authorized security research only. 
Bypassing antivirus software or other security measures is not within the scope of this project. 
It is designed for testing in controlled environments to demonstrate the feasibility and mechanics of using DoH for C2 communication **to test enterprise corporate forward proxy detection and improve any custom build signatures in SIEMs.**

# Features
**Covert Communicatio**n: Utilizes DoH to encode and disguise C2 traffic.
**Command Execution**: Supports remote execution of commands on infected Linux clients 
**Data Exfiltration**: Allows for exfiltration of data through DOH queries.
**Server and Client Implementation**: Includes both C2 server and client components.

# Initial setup

1. **Client Side** windows or Linux
    Python:
        Install Python 3.x from the official website or your package manager.
    Requests Library:
       Install the requests library using pip:
       pip install requests
2. **Server side** only Linux
Dnslib Library:
    Install the dnslib library using pip:
    pip install dnslib

3. Register domain 
Example purchasing domain using namecheap.com
![grafik](https://github.com/user-attachments/assets/adb40d21-4985-465c-864f-a286b49a2bc1)
Follow instructions on the screenshot bellow to setup the NameServer.
Replace the IP and domainname with your purchased domain
![grafik](https://github.com/user-attachments/assets/c9e9f4cf-ac77-4b31-b92d-7bfe28ed93e9)


# Architecture TODO
