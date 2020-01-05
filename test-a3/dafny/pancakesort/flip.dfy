// flips (i.e., reverses) array elements in the range [0..num]
method flip (a: array<int>, num: int)
  requires a != null && a.Length > 0
  requires 0<=num<a.Length
  modifies a
ensures forall n:: 0 <= n <= num  ==> a[n] == old(a[num-n]) 
ensures forall n:: num < n < a.Length ==> a[n] == old(a[n]);
{
  var tmp:int;

  var i := 0;
  var j := num;
  while (i < j)
    invariant 0<=i<=num/2+1
    invariant num/2<=j<=num
    invariant i+j==num
    invariant forall k3 :: 0<=k3<i ==> a[k3]==old(a[num-k3]) && a[num-k3]==old(a[k3])
 //   invariant forall k4 :: j<k4<=num ==> old(a[k4])==a[num-k4]
    invariant forall k5 :: i<=k5<=j ==> old(a[k5])==a[k5]
    invariant forall k6 :: num<k6<a.Length ==> old(a[k6])==a[k6]
    decreases j
    decreases num-i
  {
    tmp := a[i];
    a[i] := a[j];
    a[j] := tmp;
    i := i + 1;
    j := j - 1;
  }
}
