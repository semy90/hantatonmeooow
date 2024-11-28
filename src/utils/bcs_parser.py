def bcs_parser(d: dict):
    starts = d['startedAt'].split('T')
    ends = d['endedAt'].split('T')
    return f"""Название: {d['name']}
Начало: {starts[0]} {starts[1]}
Конец: {ends[0]} {ends[1]}
Состояние: {d['state']}
"""