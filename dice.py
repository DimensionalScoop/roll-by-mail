import re
import numpy as np

die_types = []
def randint(high,size=1,low=1):
    if size<0:
        dtype = np.int64
    else:
        dtype = np.uint64
    return np.random.randint(low, high, size, dtype=dtype)


class die_like:
    @classmethod
    def reduce(cls, pattern):
        return cls.pattern.sub(pattern, "")

    @classmethod
    def get_dice(cls, pattern):
        return_value = []
        dice = cls.pattern.findall(pattern)
        for i in dice:
            return_value.append(cls())
        return return_value

    def roll(self):
        raise NotImplementedError()


class polyhedral_die(die_like):
    pattern = re.compile(r"([+-]?)\s*(\d*)d(\d+)\b")

    @classmethod
    def get_dice(cls, pattern):
        dice = polyhedral_die.pattern.findall(pattern)
        return_value = []
        for die_group in dice:
            sign, number, sides = die_group
            if sign == "":
                sign = "+"
            if number == "":
                number = 1
            for i in range(int(number)):
                return_value.append(polyhedral_die(int(sides), sign))
        return return_value

    def __init__(self, sides, sign="+"):
        self.sides = sides
        self.sign = sign

    def __str__(self):
        name = "- d" if self.sign == "." else "d"
        name += str(self.sides)
        return name

    def __repr__(self):
        action = "subtracted" if self.sign == "-" else "added"
        return str(self.sides) + "-sided die that is " + action

    def roll(self):
        return randint(self.sides + 1)


class bonus(die_like):
    pattern = re.compile(r"([+-])\s*(\d+)\b")

    @classmethod
    def get_dice(cls, pattern):
        boni = bonus.pattern.findall(pattern)
        if len(boni) == 0:
            return []
        total = 0
        for i in boni:
            sign, number = i
            if sign == "+" or sign == "":
                total += int(number)
            elif sign == "-":
                total -= int(number)
        return [bonus(total)]

    def __init__(self, bonus):
        self.bonus = bonus

    def roll(self):
        return self.bonus

    def __str__(self):
        return str(self.bonus)

    def __repr__(self):
        return "static bonus of " + str(self.bonus)


class dsa_check(die_like):
    pattern = re.compile(r"dsa")

    def roll(self):
        dice = tuple(randint(21, size=3).tolist())
        return "\\[%d] \\[%d] \\[%d]" % dice

    def __repr__(self):
        return "DSA check"


class fudge(die_like):
    pattern = re.compile(r"([+-]?)\s*(\d*)dF\b")

    @classmethod
    def get_dice(cls, pattern):
        dice = fudge.pattern.findall(pattern)
        return_value = []
        for die_group in dice:
            sign, number = die_group
            if number == "":
                number = 4
            for i in range(int(number)):
                return_value.append(fudge(sign))
        return return_value

    def __init__(self, sign="+"):
        self.sign = sign

    def __str__(self):
        name = "- dF" if self.sign == "." else "dF"
        return name

    def __repr__(self):
        action = "subtracted" if self.sign == "-" else "added"
        return "fudge die that is " + action

    def roll(self):
        return randint(low=-1,high=1 + 1)


die_types.extend([polyhedral_die, bonus, dsa_check, fudge])

