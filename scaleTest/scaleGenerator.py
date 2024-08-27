import random

portSet = set()
with open( 'scaleTest/input/lookup_table.txt', 'w' ) as file:
    file.write('dstport,protocol,tag\n')
    for i in range(0, 10000):
        protocols = ["tcp", "udp", "icmp", "gre"]
        tags = ["sv_P1", "sv_P2", "sv_P3", "sv_P4", "sv_P10", "sv_P5", "email"]
        while True:
            randPort = random.randint(0, 65535)
            randProtocol = protocols[ random.randint(0, 3) ]
            key = str(randPort) + "+" + str(randProtocol)
            if key not in portSet:
                randTag = tags[ random.randint(0, 6) ]
                entry = str(randPort) + "," + str(randProtocol) + "," + randTag + "\n"
                file.write(entry)
                portSet.add( key )
                break

with open( 'scaleTest/input/flow_logs.txt', 'w' ) as file:
    template = "2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 110 6 25 20000 1620140761 1620140821 ACCEPT OK"
    templateList = template.split(' ')
    mappedPorts = list(portSet)
    srcDstProtocolCombination = set()
    protocolMap = { 'tcp': 6, 'udp': 17, 'icmp' : 1, 'gre': 47 }

    for i in range(0, 90000):
        randPortProtocol = mappedPorts[ random.randint(0, len(mappedPorts) - 1 ) ]
        key = randPortProtocol.split('+')
        dstport = key[0]
        protocol = key[1]
        while True:
            srcport = (str) (random.randint(0, 65535))
            if not srcport + "+" + dstport + "+" + protocol in srcDstProtocolCombination:
                newEntry = templateList[:]
                newEntry[5] = srcport
                newEntry[6] = dstport
                newEntry[7] = (str) ( protocolMap[ protocol ] )
                entry = " ".join(newEntry) + "\n"
                file.write(entry)
                srcDstProtocolCombination.add( srcport + "+" + dstport + "+" + protocol )
                break
           
    
