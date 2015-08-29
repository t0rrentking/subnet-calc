import sys
 
def calcIPValue(ipaddr):
        """
        Calculates the binary
        value of the ip addresse
        """
        ipaddr = ipaddr.split('.')
        value = 0
        for i in range(len(ipaddr)):
                value = value | (int(ipaddr[i]) << ( 8*(3-i) ))
        return value
 
def calcIPNotation(value):
        """
        Calculates the notation
        of the ip addresse given its value
        """
        notat = []
        for i in range(4):
                shift = 255 << ( 8*(3-i) )
                part = value & shift
                part = part >> ( 8*(3-i) )
                notat.append(str(part))
        notat = '.'.join(notat)
        return notat
 
def calcSubnet(cidr):
        """
        Calculates the Subnet
        based on the CIDR
        """
        subn = 4294967295 << (32-cidr)  # 4294967295 = all bits set to 1
        subn = subn % 4294967296        # round it back to be 4 bytes
        subn = calcIPNotation(subn)
        return subn
 
def calcCIDR(subnet):
        """
        Calculates the CIDR
        based on the SUbnet
        """
        cidr = 0
        subnet = calcIPValue(subnet)
        while subnet != 0:
                subnet = subnet << 1
                subnet = subnet % 4294967296
                cidr += 1
        return cidr
 
def calcNetpart(ipaddr,subnet):
        ipaddr = calcIPValue(ipaddr)
        subnet = calcIPValue(subnet)
        netpart = ipaddr & subnet
        netpart = calcIPNotation(netpart)
        return netpart
 
def calcMacpart(subnet):
        macpart = ~calcIPValue(subnet)
        macpart = calcIPNotation(macpart)
        return macpart
 
def calcBroadcast(ipaddr,subnet):
        netpart = calcNetpart(ipaddr,subnet)
        macpart = calcMacpart(subnet)
        netpart = calcIPValue(netpart)
        macpart = calcIPValue(macpart)
        broadcast = netpart | macpart
        broadcast = calcIPNotation(broadcast)
        return broadcast
 
def calcDefaultGate(ipaddr,subnet):
        defaultgw = calcNetpart(ipaddr,subnet)
        defaultgw = calcIPValue(defaultgw) + 1
        defaultgw = calcIPNotation(defaultgw)
        return defaultgw
 
def calcHostNum(subnet):
        macpart = calcMacpart(subnet)
        hostnum = calcIPValue(macpart) - 1
        return hostnum
       
 
def main():
        if (len(sys.argv) == 2 and '/' in sys.argv[1]):         # IPAdresse/CIDR
                ipaddr = sys.argv[1].split('/')[0]
                cidr = sys.argv[1].split('/')[1]
                subnet = calcSubnet(int(cidr))         
        elif    (len(sys.argv) == 3):                   # IPAdresse Subnet
                ipaddr = sys.argv[1]
                subnet = sys.argv[2]
                cidr = calcCIDR(subnet)
        else:
                args = ' '.join(sys.argv[1:])
                sys.exit('"' + args + '" is no valid combination of an IP and a Subnet/CIDR!')
       
        print '==============================='
        print 'IPv4:             ' + ipaddr
        print 'Netmask:          ' + subnet
        print 'CIDR:             ' + str(cidr)
        macpart = calcMacpart(subnet)
        print 'Inversed Netmask: ' + macpart
        hostnum = calcHostNum(subnet)
        print 'Hosts:            ' + str(hostnum)
        netpart = calcNetpart(ipaddr,subnet)
        print 'Network:          ' + netpart
        broadcast = calcBroadcast(ipaddr,subnet)
        print 'Broadcast:        ' + broadcast
        defaultgw = calcDefaultGate(ipaddr,subnet)
        print 'Default Gateway:  ' + defaultgw
        print '==============================='
 
if __name__ == '__main__':
        main()
