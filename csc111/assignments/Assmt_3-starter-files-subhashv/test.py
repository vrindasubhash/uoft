from a3_network import Channel, NodeAddress, Node, Packet
from a3_part4 import GreedyChannelRing, GreedyChannelTorus, GreedyChannelStar,\
    GreedyPathRing, GreedyPathTorus, GreedyPathStar
from a3_part2 import AlwaysRightRing, ShortestPathRing, ShortestPathTorus, ShortestPathStar
from a3_part3 import part3_runner

my_ring = AlwaysRightRing(5)
my_packet = Packet(0, 1, 4)
print(my_ring.transmit_packet(my_packet))

my_ring = ShortestPathRing(5)
my_packet = Packet(0, 1, 4)
print(my_ring.transmit_packet(my_packet))

my_ring = GreedyChannelRing(5)
my_packet = Packet(0, 1, 4)
print(my_ring.transmit_packet(my_packet))

my_ring = GreedyPathRing(5)
my_packet = Packet(0, 1, 4)
print(my_ring.transmit_packet(my_packet))

my_torus = ShortestPathTorus(4)
my_packet = Packet(0, (1,1), (3,3))
print(my_torus.transmit_packet(my_packet))

my_torus = GreedyChannelTorus(4)
my_packet = Packet(0, (1,1), (3,3))
print(my_torus.transmit_packet(my_packet))

my_torus = GreedyPathTorus(4)
my_packet = Packet(0, (1,1), (3,3))
print(my_torus.transmit_packet(my_packet))

my_star = ShortestPathStar(2, 4)
my_packet = Packet(0, 1, 4)
print(my_star.transmit_packet(my_packet))

my_star = GreedyChannelStar(2, 4)
my_packet = Packet(0, 1, 4)
print(my_star.transmit_packet(my_packet))

my_star = GreedyPathStar(2, 4)
my_packet = Packet(0, 1, 4)
print(my_star.transmit_packet(my_packet))

part3_runner('data/test.csv', 'route-lengths')
