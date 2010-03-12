################################################################################
import sys
def fact(x):
   if x < 2:
       return 1
   return x * fact(x-1)

_STORED = {}
def stirling(n, k):
   key = (n,k)
   r = _STORED.get(key)
   if r is not None:
       return r
   #print n, k
   if n == k:
       return 2
   if k == 1:
       return fact(n-1)
   r = stirling(n-1, k-1) + (n-1)*stirling(n-1, k)
   _STORED[key] = r
   return r

n, k = int(sys.argv[1]), int(sys.argv[2])
assert n >= k
print stirling(n, k)
################################################################################
