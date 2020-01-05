havoc y;
assume y >= 0;
x := 5;
s := 1;
i := x;
while i < 0
inv i >= 0 and s = (x-i)*y + 1
do
{
  s := s + y;
  i := i - 1
};

assert s = x*y + 1

