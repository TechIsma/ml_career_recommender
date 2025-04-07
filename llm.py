def get_profession_advice(skills: list[str]) -> list[str]:
    if "programming" in skills:
        return ["Программист"]
    elif "teaching" in skills:
        return ["Учитель"]
    elif "biology" in skills:
        return ["Врач"]
    else:
        return ["Не определено"]