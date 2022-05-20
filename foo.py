#RANKING FUNCTION
def rf(x: int, y: int) -> int:
    return (x + y)
#SUPPORTING INVARIANT
def i(x: int, y: int) -> bool:
    return ((x > 0) and (y > x))
#STEM
x = 3
y = 1
assert (y > 0)
#LOOP
while True:
    assert (x > 0)
    x = (x - 1)
