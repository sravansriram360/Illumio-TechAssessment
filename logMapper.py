import os 

class LogMapper:
    def __init__( self, directory, logFile, lookupTableFile ):
        self.dir = directory
        self.logFile = logFile
        self.lookupTableFile = lookupTableFile
        
        # Static mappings of protocol numbers, and order of entries in the log files
        self.protocolMap = { 6: 'tcp', 17: 'udp', 1: 'icmp', 47: 'gre' }
        self.logColMap = { 'dstport': 6, 'protocol': 7 }

        # Storage for intermediate data processing
        self.logs = []
        self.tagTable = {}

        # Maps each unique tag to its frequency in the log file
        self.tagCount = {}
        # Maps each unique (port, protocol) combination to its frequency in the log file
        self.portProtocolCount = {}
    
    # Generates a unique key identifier given a particular (dst_port, protocol) combination 
    def __constructLogKey( self, dst_port, protocol ):
        return dst_port + "+" + protocol
    

    '''
        Helper function for storing frequency of both 
        tags and (port, protocol) in their respective HashMaps
    '''
    def __incrementKeyCount( self, countMap, key ):
        if key not in countMap:
            countMap[ key ] = 1
        else:
            countMap[ key ] += 1
    
    # Reads and stores logs in the input file
    def __processLogFile( self ):
        with open( self.dir + '/' + "input/" + self.logFile, 'r' ) as log_file:
            for line in log_file:
                line.strip()
                log = line.split(' ')
                self.logs.append(log)
    
    '''
        Reads and stores lookup table from the input file
        Maps the (dst_port, protocol) combination to a case insensitive tag in a HashMap
    ''' 
    def __processLookupTableFile( self ):
        with open( self.dir + '/' + "input/" + self.lookupTableFile, 'r') as log_file:
            for line in list(log_file)[1:]:
                line.strip()
                tagMap = line.split(',')

                dst_port = tagMap[0]
                protocol = tagMap[1].lower()
                tag = tagMap[2]
                
                key = self.__constructLogKey( dst_port, protocol )
                finalTag = tag.lower()
                finalTag = finalTag.strip()
                self.tagTable[key] = finalTag

    # Processes both input files
    def processInputFiles( self ):
        self.__processLogFile()
        self.__processLookupTableFile()
    
    '''
        Intermediate function for mapping each log to its appropriate tag,
        storing frequency of each unique tag observed, as well as storing 
        frequency of each unique (dst_port, protocol) combination observed
    '''
    def mapLogsToTags( self ):
        for log in self.logs:
            dst_port = log[ self.logColMap[ 'dstport' ] ]
            protocolInt = (int) ( log[ self.logColMap[ 'protocol' ] ] )
            protocol = self.protocolMap[ protocolInt ]
            logKey = self.__constructLogKey( dst_port, protocol )

            if logKey in self.tagTable:
                tag = self.tagTable[ logKey ]
                self.__incrementKeyCount( self.tagCount, tag )
                self.__incrementKeyCount( self.portProtocolCount, logKey )
            else:
                self.__incrementKeyCount( self.tagCount, 'Untagged' )
    
    '''
        Writes to an output file contianing info regarding the frequency of 
        each tag (as well as those that are Untagged). Outputs an ERROR message if the total 
        cumulative count of all tags is not equal to the total number of logs.
    '''
    def __outputTagCount( self ):
        totalSum = 0
        with open( self.dir + '/output/tagCount.txt', 'w' ) as file:
            file.write("Tag,Count\n")
            for tag, count in self.tagCount.items():
                entry = tag + "," + str(count) + "\n"
                totalSum += count
                file.write(entry)
        if totalSum != len(self.logs):
            print('ERROR: tags cumulative count ', totalSum, ' is not equal to the number of logs', len(logs))
    
    '''
        Writes to an output file contianing info regarding the frequency of 
        each unique (port, protocol) combination observed. Outputs an ERROR message if the total 
        cumulative count of all (port, protocol) combinations is not equal 
        to total number of logs - untagged counts.
    '''
    def __outputPortProtocolCount( self ):
        expectedTotalSum = len(self.logs) 
        if 'Untagged' in self.tagCount:
            expectedTotalSum -= self.tagCount['Untagged']

        actualTotalSum = 0
        with open( self.dir + '/output/port-protocolCount.txt', 'w' ) as file:
            file.write("Port,Protocol,Count\n")
            for portProtocol, count in self.portProtocolCount.items():
                key = portProtocol.split('+')
                port = key[0]
                protocol = key[1]
                entry = port + "," + protocol + "," + str(count) + "\n"
                actualTotalSum += count
                file.write(entry)
        
        if actualTotalSum != expectedTotalSum:
            print('ERROR: (port, protocol) cumulative count ', actualTotalSum, ' is not equal to expected cumulative count', expectedTotalSum)
    
    # Writes to both output files to output directory test/output/...
    def writeToOuputFiles( self ):
        directory_path = self.dir + "/output"
        os.makedirs( directory_path, exist_ok=True )
        self.__outputTagCount()
        self.__outputPortProtocolCount()

if __name__ == "__main__":

    inputFiles = [ 'flow_logs.txt', 'lookup_table.txt' ]

    tests = [ 'singleTagMappingAllPresentTest/', 'singleTagMappingSomeUntaggedTest/', 'duplicateTagMappingAllPresentTest/', 
              'duplicateTagMappingSomeUntaggedTest/', 'duplicatePortProtocolTest/', 'caseSensitiveTest/', 'scaleTest/' ]

    for test in tests:
        logMapper = LogMapper( test, inputFiles[0], inputFiles[1] )
        logMapper.processInputFiles()
        logMapper.mapLogsToTags()
        logMapper.writeToOuputFiles()
