// returns an index of the largest element of array 'a' in the range [0..n)
method findMax (a : array<int>, n : int) returns (r:int)
  requires a != null && a.Length > 0
  requires 0<n<=a.Length
  ensures 0<=r<n
  ensures forall k :: 0<=k<n ==> a[r]>=a[k] 
{
  var mi;
  var i;
  mi := 0;
  i := 0;
  while (i < n)
     invariant 0<=i<=n
     invariant 0<=mi<n
     invariant forall k2 :: 0<=k2<i ==> a[mi]>=a[k2]
     decreases n-i
  {
    if (a[i] > a[mi])
    { mi := i; }
    i := i + 1;
  }
  return mi;
}
