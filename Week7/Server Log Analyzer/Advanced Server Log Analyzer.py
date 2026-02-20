import os
import re
import logging
from collections import defaultdict

def analyze_server_logs():
    #file paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(script_dir, 'server_logs.txt')
    error_log_path = os.path.join(script_dir, 'error_log.txt')
    security_log_path = os.path.join(script_dir, 'security_incidents.txt')
    system_log_path = os.path.join(script_dir, 'analyzer_system.log')

    #configure logging
    logging.basicConfig(
        filename=system_log_path, 
        level=logging.WARNING,
        format='%(asctime)s - %(levelname)s - %(message)s')

    #forgiving Regex to extract Apache log components
    log_pattern = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+).*?\[(?P<timestamp>.*?)\].*?"(?P<method>[A-Z]+)\s+(?P<url>\S+).*?"\s+(?P<status>\d{3})\s+.*?"(?P<agent>.*?)"'
    )

    ip_failures = defaultdict(int)

    print("Starting Server Log Analysis...")
    
    #check if the input file actually exists before opening it
    if not os.path.exists(log_file_path):
        print(f"Critical Error: Could not find '{log_file_path}'.")
        print("Please make sure you created 'server_logs.txt' and saved it in the same folder!")
        logging.critical(f"Input file missing: {log_file_path}")
        return

    try:
        #open all files with utf-8 encoding to prevent hidden character errors
        with open(log_file_path, 'r', encoding='utf-8') as infile, \
             open(error_log_path, 'w', encoding='utf-8') as error_out, \
             open(security_log_path, 'w', encoding='utf-8') as security_out:

            for line in infile:
                # Skip empty lines
                if not line.strip():
                    continue
                    
                #catch parsing errors
                try:
                    match = log_pattern.search(line)
                    if not match:
                        logging.debug(f"Malformed log entry skipped: {line.strip()}")
                        continue
                    
                    #named groups
                    data = match.groupdict()
                    status_code = int(data['status'])
                    ip = data['ip']
                    agent = data['agent'].lower()

                    #Error Logs (4xx and 5xx codes)
                    if status_code >= 400:
                        error_out.write(line)

                    #Security Monitorin
                    is_incident = False
                    reasons = []

                    #check for failed authentication and Brute Force
                    if status_code == 401:
                        ip_failures[ip] += 1
                        reasons.append("Failed authentication")
                        
                        #3 or more failures from the same IP, flag as brute force
                        if ip_failures[ip] >= 3:
                            reasons.append("Brute force attack detected")
                            logging.warning(f"Brute force detected from IP: {ip}")
                            is_incident = True
                            
                    #check for forbidden access attempts
                    elif status_code == 403:
                         reasons.append("Forbidden access attempt")
                         is_incident = True

                    #check for suspicious user agents
                    if 'sqlmap' in agent or 'curl' in agent:
                        reasons.append("Suspicious user agent")
                        is_incident = True

                    #write to security incidents file
                    if is_incident or (status_code == 401 and ip_failures[ip] >= 3):
                        security_out.write(f"[{data['timestamp']}] IP: {ip} | Status: {status_code} | Triggers: {', '.join(reasons)} | URL: {data['url']}\n")

                except Exception as e:
                    logging.error(f"Error parsing line: {line.strip()} | Context: {str(e)}")

        print("Analysis complete! Check your folder for 'error_log.txt' and 'security_incidents.txt'.")

    except PermissionError:
        print("Error: Permission denied to write the output files.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    analyze_server_logs()