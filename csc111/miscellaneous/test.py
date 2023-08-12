from __future__ import annotations

class A:
    a: A




# class AbstractNetwork1:
#     _nodes: dict[str, str]
#
#     def __init__(self) -> None:
#         print('checking')
#         self._nodes = {}
#
#     def add_node(self, address: str) -> str:
#         self._nodes[address] = address
#         return address
#
# class AbstractRing1(AbstractNetwork1):
#     def __init__(self, k: int) -> None:
#         super().__init__()
#         self.add_node('abc')

#
# k = 5
# start = 3
# end = 1
#
# a = end - start
# a1 = abs(a)
# b = k - a1
#
# if a > 0:
#     if a1 <= b:
#         print('right')
#     else:
#         print('left')
# else:
#     if a1 <= b:
#         print('left')
#     else:
#         print('right')
