import dice


def pattern_to_dice(dice_pattern:str):
    shaker = []
    for die in dice.die_types:
        shaker.extend(die.get_dice(dice_pattern))
        pattern = die.reduce(dice_pattern)
    if pattern.strip()!="":
        raise ValueError("Unknown dice pattern: "+pattern)
    return shaker