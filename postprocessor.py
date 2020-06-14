import dice

ladder = {
        8:"Legendary",
        7:"Epic",
        6:"Fantastic",
        5:"Superb",
        4:"Great",
        3:"Good",
        2:"Fair",
        1:"Average",
        0:"Mediocre",
        -1:"Poor",
        -2:"Terrible",
    }

def fate(shaker, result_numbers, result_strings):
    result = sum(result_numbers)

    for die in shaker:
        if not isinstance(die,(dice.fudge,dice.bonus)):
            return None # this is not a Fate die roll
    try:
        quality = " ("+ladder[result]+")"
    except IndexError:
        quality = ""
    if result==0:
        return ["±0"+quality]
    elif result<0:
        return ["-"+str(-result)+quality]
    elif result>0:
        return ["+"+str(result)+quality]


postprocessors = [fate]