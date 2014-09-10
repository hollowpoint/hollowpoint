from inventory.models import NetDevice

cisco = NetDevice.objects.filter(manufacturer='Cisco Systems', model='3745')

count = 16
names = []
for i in range(1, 16 + 1):
    names.append('core-c%s.lab.hollow.pt' % i)
    names.append('edge-c%s.lab.hollow.pt' % i)

for c in cisco:
    c.node_name = names.pop()
    print c.node_name
