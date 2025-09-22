import xml.etree.ElementTree as ET


def parse_nmap_xml(path):

    tree = ET.parse(path)
    root = tree.getroot()
    host = root.find('host')
    result = {"ports": []}
    for ports in root.findall('.//port'):
        portid = ports.get('portid')
        proto = ports.get('protocol')
        state = ports.find('state').get('state')
        svc = ports.find('service')
        svcname = svc.get('name') if svc is not None else ''
        version = svc.get('product') + ' ' + svc.get('version') if svc is not None and svc.get('product') else ''
        result['ports'].append({
            'port': int(portid), 'protocol': proto, 'state': state,
            'service': svcname, 'version': version
        })
    return result
