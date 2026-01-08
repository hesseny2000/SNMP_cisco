from pysnmp.hlapi import *

SNMP_HOST = '10.20.30.40'
SNMP_COMMUNITY = 'MY_SNMP_COMMUNITY'
SNMP_PORT = 161

OIDS = {
    'nbr_ip': '1.3.6.1.2.1.14.10.1.1',
    'nbr_if': '1.3.6.1.2.1.14.10.1.2',
    'nbr_router_id': '1.3.6.1.2.1.14.10.1.3',
    'nbr_state': '1.3.6.1.2.1.14.10.1.6',
    'nbr_dead': '1.3.6.1.2.1.14.10.1.7',
    'nbr_priority': '1.3.6.1.2.1.14.10.1.5'
}

STATE_MAP = {
    '1': 'Down',
    '2': 'Attempt',
    '3': 'Init',
    '4': '2-Way',
    '5': 'Exchange',
    '6': 'Loading',
    '7': 'Full'
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

# SNMP Walk
nbr_ip = snmp_walk(OIDS['nbr_ip'])
nbr_if = snmp_walk(OIDS['nbr_if'])
nbr_router_id = snmp_walk(OIDS['nbr_router_id'])
nbr_state = snmp_walk(OIDS['nbr_state'])
nbr_dead = snmp_walk(OIDS['nbr_dead'])
nbr_priority = snmp_walk(OIDS['nbr_priority'])

# Print CLI-like Table
print(f"{'Neighbor ID':<12}{'Pri':<5}{'State':<12}{'Dead Time(s)':<12}{'IP Address':<15}{'Interface':<10}")
print("-"*70)

for idx in nbr_ip:
    router_id = nbr_router_id.get(idx, 'N/A')
    ip = nbr_ip.get(idx)
    state = STATE_MAP.get(nbr_state.get(idx, '1'), 'Unknown')
    dead = nbr_dead.get(idx, '0')
    priority = nbr_priority.get(idx, '0')
    if_idx = nbr_if.get(idx, '0')
    print(f"{router_id:<12}{priority:<5}{state:<12}{dead:<12}{ip:<15}{if_idx:<10}")
