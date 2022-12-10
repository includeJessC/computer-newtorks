import argparse
import re
import subprocess
import ipaddress

SUM_HEADERS_SIZE = 28
REG_FOR_HOST = re.compile(
    r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
    r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
    r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
    r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
)
ICMP_DISABLE = subprocess.run(
    ["cat", "/proc/sys/net/ipv4/icmp_echo_ignore_all"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True,
)

def main():
    parser = argparse.ArgumentParser(description='FIND PMTUD')
    parser.add_argument('host')
    args = parser.parse_args()
    host = args.host
    try:
        if REG_FOR_HOST.match(host) or ipaddress.ip_address(host):
            if ICMP_DISABLE.stdout == 1:
                print("SOMETHING WENT WRONG")
                exit(1)
            l, r = 0, 9001 - SUM_HEADERS_SIZE
            res = l
            while l + 1 < r:
                m = (l + r) // 2
                process = subprocess.run(
                    ["ping", host, "-M", "do", "-s", str(m), "-c", "2"],
                )
                if process.returncode == 0:
                    l = m
                elif process.returncode == 1:
                    r = m
                else:
                    print("SOMETHING WENT WRONG")
                    exit(1)
            res = l
            print(res + SUM_HEADERS_SIZE)
            return
        else:
            print("SOMETHING WRONG WITH HOST, IT DOESNT MATHC REGULAR")
            exit(1)
    except Exception as e:
        print("SOMETHING WRONG WITH HOST, EXCEPTION:" + str(e))
        exit(1)
    return

if __name__ == '__main__':
    main()
