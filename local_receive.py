import socket
import json
import os
import time

def receive_json_data(server_ip, port=5000):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server
        client_socket.connect((server_ip, port))
        print(f"Connected to server at {server_ip}:{port}")
        
        # Create received_data directory if it doesn't exist
        received_data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'received_data')
        os.makedirs(received_data_dir, exist_ok=True)
        
        while True:
            try:
                # Receive data
                data = b""
                while True:
                    chunk = client_socket.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                
                if not data:
                    continue
                
                # Decode and parse JSON data
                json_data = json.loads(data.decode('utf-8'))
                
                # Save received data to a file
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                output_file = os.path.join(received_data_dir, f'received_data_{timestamp}.json')
                
                with open(output_file, 'w') as f:
                    json.dump(json_data, f, indent=4)
                
                print(f"Received and saved data to {output_file}")
                
                # Send acknowledgment
                client_socket.sendall(b"Data received successfully")
                
            except json.JSONDecodeError:
                print("Error: Invalid JSON data received")
                continue
            except Exception as e:
                print(f"Error: {str(e)}")
                continue
                
    except KeyboardInterrupt:
        print("\nClient shutting down...")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    # Replace 'SERVER_IP' with the actual IP address of the sender device
    SERVER_IP = '192.168.1.100'  # Change this to the sender's IP address
    receive_json_data(SERVER_IP) 