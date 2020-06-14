import parser
from dice import *

d = polyhedral_die
tests = {
    "d6": [d(6)],
    "3d10 + 5": [d(10), d(10), d(10), bonus(5)],
    "1d20 -3": [d(20), bonus(-3)],
    "-10+d20": [d(20), bonus(-10)],
    "d6+d6 + d8 -d4 -1": [d(6), d(6), d(8), d(4, "-"), bonus(-1)],
    "dsa": [dsa_check()],
    "d4+dsa":[d(4),dsa_check()],
    "2dF":[fudge(),fudge()],
    "dF":[fudge(),fudge(),fudge(),fudge()],
    "dF+3":[fudge(),fudge(),fudge(),fudge(),bonus(3)],
    "4d4+1d20-1dF":[d(4),d(4),d(4),d(4),d(20),fudge("-")]
}

#%%
for pattern, desired in tests.items():
    print(pattern,end="")
    actual = parser.pattern_to_dice(pattern)
    
    assert np.array([str(i)!="" for i in pattern]).all()
    desired_str = sorted(str(i) for i in desired)
    actual_str = sorted(str(i) for i in actual)
    np.testing.assert_equal(desired_str,actual_str)
    print(" passed",parser.roll(actual))