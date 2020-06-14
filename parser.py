import dice
from postprocessor import postprocessors, default_postprocessing

def pattern_to_dice(dice_pattern:str):
    shaker = []
    for die in dice.die_types:
        shaker.extend(die.get_dice(dice_pattern))
        pattern = die.reduce(dice_pattern)
    if pattern.strip()!="":
        raise ValueError("Unknown dice pattern: "+pattern)
    return shaker

def roll(shaker):
    numbers = []
    strings = []
    for die in shaker:
        result = die.roll()
        if isinstance(result,str):
            strings.append(result)
        else:
            numbers.append(result)
    
    for p in postprocessors:
        result = p(shaker,numbers,strings)
        if result is not None:
            return result
    
    return default_postprocessing(shaker,numbers,strings)
    

def handle_dice_command(chat_message):
    shaker = pattern_to_dice(chat_message)
    result = roll(shaker)
    return result