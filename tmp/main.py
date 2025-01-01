def decimal_to_binary(decimal):
    binary = ""
    while decimal:
        d, m = decimal//2, decimal%2
        decimal = d
        binary += str(m)
    return binary[::-1]
    
def decimal_to_octet(decimal):
    octet = ""
    while decimal:
        d, m = decimal//2, decimal%2
        decimal = d
        octet += str(m)
    return octet.zfill(8)[::-1]

def decimal_addr_to_binary_addr(decimal_addr):
    binary_addr = ""
    for decimal in decimal_addr.split("."):
        binary_addr += decimal_to_octet(int(decimal))
    return binary_addr

def binary_addr_to_decimal_addr(binary_addr):
    decimal_addr = []
    for i in range(4):
        binary = binary_addr[8*i:8*i+8]
        decimal_addr.append(str(binary_to_decimal(binary)))
    return ".".join(decimal_addr)

def get_number_of_hosts(prefix):
    power = 32-prefix
    return 2**power

def binary_to_decimal(binary):
    decimal = 0
    for power, bit in enumerate(binary[::-1]):
        decimal += int(bit)*(2**power)
    return decimal

def prefix_to_subnetmask(prefix):
    subnetmask = []
    tmp = "1"*prefix + "0"*(32-prefix)
    for i in range(4):
        binary = tmp[8*i:8*i+8]
        subnetmask.append(str(binary_to_decimal(binary)))
    return ".".join(subnetmask)


def main():
    input_net_addr = "192.168.10.128"
    input_prefix = 25

    # input_net_addr = "192.168.128.0"
    # input_prefix = 23

    # input_net_addr = "192.168.128.0"
    # prefix = 17

    binary_net_addr = decimal_addr_to_binary_addr(input_net_addr)

    for power, prefix in enumerate(range(input_prefix, 31)):
        # print(prefix)
        network_count = 2**power
        print("네트워크 갯수: ", network_count, ",", "(분할", prefix-input_prefix, "회)")
        
        subnetmask = prefix_to_subnetmask(prefix)
        number_of_hosts = get_number_of_hosts(prefix)
        number_of_usable_hosts = number_of_hosts - 2
        # print("네트워크 주소:", )
        print("서브넷 마스크:", subnetmask)
        print("프리픽스:", prefix)
        print("규모:", number_of_hosts)
        print("가용규모:", number_of_usable_hosts)

        print("네트워크 주소\t\t가용 주소\t\t\t\t브로드캐스트 주소")
        for i in range(network_count):
            hosts_start_binary = f"{binary_net_addr[:prefix-(prefix-input_prefix)]}{decimal_to_binary(i).zfill(prefix-input_prefix)}{'0'*(32-prefix)}"
            hosts_end_binary = f"{binary_net_addr[:prefix-(prefix-input_prefix)]}{decimal_to_binary(i).zfill(prefix-input_prefix)}{'1'*(32-prefix)}"
            usable_hosts_start_binary = bin(int(hosts_start_binary, 2) + int("1", 2))[2:]
            usable_hosts_end_binary = bin(int(hosts_end_binary, 2) - int("1", 2))[2:]
            if prefix <= 30:
                print(f"{binary_addr_to_decimal_addr(hosts_start_binary)}\t\t{binary_addr_to_decimal_addr(usable_hosts_start_binary)}\t~ {binary_addr_to_decimal_addr(usable_hosts_end_binary)}\t{binary_addr_to_decimal_addr(hosts_end_binary)}")
            else:
                print(f"{binary_addr_to_decimal_addr(hosts_start_binary)}\t\tNone\t{binary_addr_to_decimal_addr(hosts_end_binary)}")
            

        # if power == 3:
        #     break
        
        print("\n")

print("\n")
print("\n")
print("\n")

if __name__ == "__main__":
    main()