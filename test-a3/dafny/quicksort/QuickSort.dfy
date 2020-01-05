include "part.dfy"


method qsort(a:array<int>, l:nat, u:nat)
  requires a != null;
  requires l <= u < a.Length;
  modifies a;

  ensures sorted_between(a, l, u+1);

{
  // complete the code for quicksort and verify the implementation
  if(l<=u):
      invariant 0<=l<＝u<a.Length
      invariant sorted_between(a, l, u+1)
    { var pivot := partition(a, l, u);
      qsort(a, l, pivot-1);
      qsort(a, pivot+1, u);
}
