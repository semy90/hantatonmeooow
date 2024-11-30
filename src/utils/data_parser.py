def data_parser(s: str):
    s = s.split('\n')
    tmp1 = s[5].split()
    tmp1 = f"{tmp1[0]}T{tmp1[1]}:00"
    tmp2 = s[7].split()
    tmp2 = f"{tmp2[0]}T{tmp2[1]}:00"
    print(tmp1)
    print(tmp2)
    d = {
        'name': s[0],
        'isMicrophoneOn': s[1].lower() == 'да',
        'isVideoOn': s[2].lower() == 'да',
        'isWaitingRoomEnabled': s[3].lower() == 'да',
        'participantsCount': s[4],
        'startedAt': tmp1,
        'durationx': s[6],
        'sendNotificationsAt': tmp2,
        'state': 'booked'
    }
    return d



def meet_parser(d:dict):
    s = f'''<b>Название</b>: {d['name']}
🕐Время начала: {d['startedAt'].split('T')[0]} {d['startedAt'].split('T')[1]}
🕘Время конца: {d['endedAt'].split('T')[0]} {d['endedAt'].split('T')[1]}
⏳Длительность: {d['duration']}
😎Организатор: {d['organizedUser']['lastName']} {d['organizedUser']['firstName']} {d['organizedUser']['middleName']}
📧Почта организатора: {d['organizedUser']['email']}
'''
    return s
def meet_parser1(d:dict):
    s = f'''<b>Название</b>: {d['name']}
🕐Время начала: {d['startedAt'].split('T')[0]} {d['startedAt'].split('T')[1]}
🕘Время конца: {d['endedAt'].split('T')[0]} {d['endedAt'].split('T')[1]}
⏳Длительность: {d['duration']}
'''
    return s