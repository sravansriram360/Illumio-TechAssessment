# Illumio-TechnicalAssessment


## Assumptions
1. The program only supports default log format, not custom and the only version that is supported is 2. 
2. The input files (both the log file and the lookup table file) do not contain duplicate entries.
3. We only support 4 protocols (TCP, UDP, ICMP, GRE) - This is to avoid hardcoding the integer to protocol string mapping of all protocols.
4. All tags (and protocol strings) are output in their lowercase form. For example, "sv_P1", "Sv_P1", "SV_P1" are all the same tags and are mapped to the output tag "sv_p1".

## Testing

1. singleTagMappingAllPresentTest: This test provides as input multiple different logs, each with a unique (dst_port, protocol) combination, all of which matches to unique tags in the lookup table.
2. singleTagMappingSomeUntaggedTest: This test provides as input multiple different logs, each with a unique (dst_port, protocol) combination, some of which match to unique tags in the lookup table. We expect to see 2 Untagged rows appear in the output. This test also ensures that certain (port, protocol) combinations do not show up in the output if a match is not present in the lookup table.
3. duplicateTagMappingAllPresentTest: This test provides as input multiple different logs, with different (dst_port, protocol) combinations. Some of these (dst_port, protocol) combinations are mapped to the same tag in the lookup table. This test ensures that the tag count shows up accurately even though the same tag is mapped to different (dst_port, protocol)s that show up in the logs.
4. duplicateTagMappingAllPresentTest: This test provides the same coverage as the duplicateTagMappingAllPresentTest but also includes logs with (dst_port, protocol)s that are not present in the lookup table. We expect to see the appropriate count of Untagged rows appear in the output.
5. duplicatePortProtocolTest: This test provides an input multiple different logs, with different (dst_port, protocol) combinations. Some of these (dst_port, protocol) combinations are found multiple times in the flow logs. We expect to see the appropriate frequency of these (dst_port, protocol) combinations in the output. We additionally ensure that (dst_port, protocol)s that are not matched to a tag in the lookup table do not show up in the output.
6. caseSensitiveTest: This test maps two different (dst_port, protocol) combinations to the same tag (one to sv_P1 and another to SV_P1). This test ensures that both these tags map to sv_p1 to ensure case insensitivity and do not show up as different tags in the output.
7. scaleTest: This test uses a 10 MB flow log file and 10,000 row lookup table file to ensure that the program runs efficiently and quickly.

