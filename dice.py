import re
import numpy as np

die_types = []

class die_like:
    @classmethod
    def reduce(cls, pattern):
        return cls.pattern.sub(pattern,"")


    def kind():
        """How the roll results should be treated:
        add: add result to total
        single: result is never added but stated on its own"""
        return "add"

    def roll(self):
        raise NotImplementedError()




class polyhedral_die(die_like):
    pattern = re.compile(r"([+-]?)\s*(\d*)d(\d+)")
    
    @staticmethod
    def get_dice(pattern):
        dice = polyhedral_die.pattern.findall(pattern)
        return_value = []
        for die_group in dice:
            sign, number, sides = die_group
            if sign=="": sign="+"
            if number=="": number=1
            for i in range(int(number)):
                return_value.append(polyhedral_die(int(sides),sign))
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
        return np.random.randint(1, self.sides + 1)

class bonus(die_like):
    pattern = re.compile(r"([+-])\s*(\d+)\b")
    
    @staticmethod
    def get_dice(pattern):
        boni = bonus.pattern.findall(pattern)
        if len(boni)==0: return []
        total = 0
        for i in boni:
            sign, number = i
            if sign=="+" or sign == "":
                total += int(number)
            elif sign=="-":
                total -= int(number)
        return [bonus(total)]
        

    def __init__(self, bonus):
        self.bonus=bonus

    def roll(self):
        return self.bonus
    
    def __str__(self):
        return str(self.bonus)
    
    def __repr__(self):
        return "static bonus of "+str(self.bonus)


die_types.extend([
    polyhedral_die,
    bonus
])