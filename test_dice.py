import parser
from dice import *

d = polyhedral_die
tests = {
    "d6": [d(6)],
    "3d10 + 5": [d(10), d(10), d(10), bonus(5)],
    "1d20 -3": [d(20), bonus(-3)],
    "-10+d20": [d(20), bonus(-10)],
    "d6+d6 + d8 -d4 -1": [d(6), d(6), d(8), d(4, "-"), bonus(-1)],
}

#%%
for pattern, desired in tests.items():
    print(pattern,end="")
    actual = parser.pattern_to_dice(pattern)
    
    assert np.array([str(i)!="" for i in pattern]).all()
    desired = sorted(str(i) for i in desired)
    actual = sorted(str(i) for i in actual)
    np.testing.assert_equal(desired,actual)
    print(" passed")