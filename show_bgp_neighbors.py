from pysnmp.hlapi import *

SNMP_HOST = '10.20.30.1'
SNMP_COMMUNITY = 'MY-0SNMP_COMMUNITY'
SNMP_PORT = 161

OIDS = {
    'peer_ip': '1.3.6.1.2.1.15.3.1.7',
    'peer_remote_as': '1.3.6.1.2.1.15.3.1.9',
    'peer_state': '1.3.6.1.2.1.15.3.1.2',
    'prefixes': '1.3.6.1.2.1.15.3.1.12',
    'msgs_in': '1.3.6.1.2.1.15.3.1.13',
    'msgs_out': '1.3.6.1.2.1.15.3.1.14'
}

STATE_MAP = {
    '1': 'Idle',
    '2': 'Connect',
    '3': 'Active',
    '4': 'OpenSent',
    '5': 'OpenConfirm',
    '6': 'Established'
}

def snmp_walk(oid):
    result = {}
    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in nextCmd(SnmpEngine(),
                              CommunityData(SNMP_COMMUNITY, mpModel=1),
                              UdpTransportTarget((SNMP_HOST, SNMP_PORT)),
                              ContextData(),
                              ObjectType(ObjectIdentity(oid)),
                              lexicographicMode=False):
        if errorIndication:
            print(errorIndication)
            break
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
            break
        else:
            for varBind in varBinds:
                idx = str(varBind[0]).split('.')[-1]
                result[idx] = str(varBind[1])
    return result

# Walk all BGP neighbors
peer_ip = snmp_walk(OIDS['peer_ip'])
peer_as = snmp_walk(OIDS['peer_remote_as'])
peer_state = snmp_walk(OIDS['peer_state'])
peer_prefixes = snmp_walk(OIDS['prefixes'])
msgs_in = snmp_walk(OIDS['msgs_in'])
msgs_out = snmp_walk(OIDS['msgs_out'])

# Print CLI-like Table
print(f"{'Neighbor IP':<15}{'Remote AS':<10}{'State':<12}{'Prefixes':<8}{'Msg In':<8}{'Msg Out':<8}")
print("-"*70)

for idx in peer_ip:
    ip = peer_ip[idx]
    state = STATE_MAP.get(peer_state.get(idx, '1'), 'Unknown')
    remote_as = peer_as.get(idx, '0')
    prefixes = peer_prefixes.get(idx, '0')
    in_msgs = msgs_in.get(idx, '0')
    out_msgs = msgs_out.get(idx, '0')
    print(f"{ip:<15}{remote_as:<10}{state:<12}{prefixes:<8}{in_msgs:<8}{out_msgs:<8}")
