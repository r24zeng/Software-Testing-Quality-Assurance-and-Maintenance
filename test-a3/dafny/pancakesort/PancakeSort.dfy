include "flip.dfy"
include "findmax.dfy"


method pancakeSort (a : array<int>)
  modifies a;
  requires a != null && a.Length > 0
  ensures forall i, j :: 0 <= i <= j < a.Length ==> a[i] <= a[j];
{
  var curr_size := a.Length;
  while (curr_size > 1)
    invariant 1<= curr_size <=a.Length
    invariant forall i, j :: curr_size<=i<=j<a.Length ==> a[i]<=a[j]
    invariant forall i, j :: 0<=i<curr_size<=j<a.Length ==> a[i]<=a[j]
    decreases curr_size
  {
    var mi := findMax (a, curr_size);
    if (mi != curr_size - 1)
    {
      flip (a, mi);
      flip (a, curr_size -1);
    }
    curr_size := curr_size - 1;
  }
}
