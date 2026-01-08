#show l2vpn xconnect
from pysnmp.hlapi import *

SNMP_HOST = '10.20.30.40'
SNMP_COMMUNITY = 'MY_SNMP_COMMUNITY'
SNMP_PORT = 161

# OIDs from CISCO-L2VPN-MIB
XCONNECT_NAME_OID = '1.3.6.1.4.1.9.10.108.1.1.1.1.1'
XCONNECT_TYPE_OID = '1.3.6.1.4.1.9.10.108.1.1.1.1.2'
XCONNECT_LOCAL_IF_OID = '1.3.6.1.4.1.9.10.108.1.1.1.1.3'
XCONNECT_PEER_OID = '1.3.6.1.4.1.9.10.108.1.1.1.1.4'
XCONNECT_ADMIN_OID = '1.3.6.1.4.1.9.10.108.1.1.1.1.5'
XCONNECT_OPER_OID = '1.3.6.1.4.1.9.10.108.1.1.1.1.6'

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

# SNMP Walks
x_names = snmp_walk(XCONNECT_NAME_OID)
x_types = snmp_walk(XCONNECT_TYPE_OID)
x_local_if = snmp_walk(XCONNECT_LOCAL_IF_OID)
x_peer = snmp_walk(XCONNECT_PEER_OID)
x_admin = snmp_walk(XCONNECT_ADMIN_OID)
x_oper = snmp_walk(XCONNECT_OPER_OID)

# Print CLI-like Table
print(f"{'Name':<15}{'Type':<10}{'Local IF':<20}{'Remote PE':<15}{'Admin':<10}{'Oper':<10}")
print("-"*85)

for idx, name in x_names.items():
    typ = x_types.get(idx, '-')
    local_if = x_local_if.get(idx, '-')
    peer = x_peer.get(idx, '-')
    admin = 'Enabled' if x_admin.get(idx, '2') == '1' else 'Disabled'
    oper = 'Up' if x_oper.get(idx, '2') == '1' else 'Down'
    print(f"{name:<15}{typ:<10}{local_if:<20}{peer:<15}{admin:<10}{oper:<10}")
