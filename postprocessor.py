import dice

ladder = {
    8: "Legendary",
    7: "Epic",
    6: "Fantastic",
    5: "Superb",
    4: "Great",
    3: "Good",
    2: "Fair",
    1: "Average",
    0: "Mediocre",
    -1: "Poor",
    -2: "Terrible",
}


def fate(shaker, result_numbers, result_strings):
    result = sum(result_numbers)

    for die in shaker:
        if not isinstance(die, (dice.fudge, dice.bonus)):
            return None  # this is not a Fate die roll

    visible_dice = []
    for die, num in zip(shaker, result_numbers):
        if isinstance(die, dice.fudge):
            if num == 1:
                symbol = "+"
            elif num == 0:
                symbol = "∙"
            elif num == -1:
                symbol = "−"
            else:
                raise Exception("This is not a Fate die!")
            visible_dice.append(symbol)

    bonus = ""
    for die, num in zip(shaker, result_numbers):
        if isinstance(die, dice.bonus):
            bonus = " + " + str(num) if num >= 0 else " - "+str(abs(num))

    result_text = "\\[ " + " ".join(visible_dice) + " ]" + bonus + "\n"

    try:
        quality = "* (" + ladder[result] + ")"
    except KeyError:
        quality = ""
    if result == 0:
        result_text += "±0" + quality + "*\n"
    elif result < 0:
        result_text += "-" + str(-result) + quality + "*\n"
    elif result > 0:
        result_text += "+" + str(result) + quality + "*\n"

    return result_text


def dsa(shaker, result_numbers, result_strings):
    for die in shaker:
        if not isinstance(die, (dice.dsa_check)):
            return None  # this is not a Fate die roll
    return default_postprocessing(
        shaker, result_numbers, result_strings, suppress_single_die_display=True
    )


def default_postprocessing(shaker, numbers, strings, suppress_single_die_display=False):
    return_value = ""
    if not suppress_single_die_display:
        return_value += "\[" + ", ".join(str(i) for i in shaker) + "]\n"
    if len(numbers) > 1:
        return_value += join_numbers(numbers) + "\n"
    if strings:
        return_value += "\n".join(strings) + "\n"
    if numbers:
        return_value += "*Σ " + str(sum(numbers)) + "*"
    return return_value


def join_numbers(numbers):
    return_value = ""
    for i, num in enumerate(numbers):
        if i == 0:
            if num < 0:
                return_value = "-" + str(-num)
            else:
                return_value = str(num)
        else:
            sign = "+" if num >= 0 else "-"
            return_value += " " + sign + " " + str(abs(num))
    return return_value


postprocessors = [fate, dsa]
