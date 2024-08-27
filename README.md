# Illumio-TechnicalAssessment


## Assumptions
1. The program only supports default log format, not custom and the only version that is supported is 2. 
2. The input files (both the log file and the lookup table file) do not contain duplicate entries.
3. We only support 4 protocols (TCP, UDP, ICMP, GRE) - This is to avoid hardcoding the integer to protocol string mapping of all protocols.
4. All tags (and protocol strings) are output in their lowercase form. For example, "sv_P1", "Sv_P1", "SV_P1" are all the same tags and are mapped to the output tag "sv_p1".

5. 

