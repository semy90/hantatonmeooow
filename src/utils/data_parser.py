def data_parser(s: str):
    s = s.split('\n')
    tmp1 = s[5].split()
    tmp1 = f"{tmp1[0]}T{tmp1}:00"
    tmp2 = s[7].split()
    tmp2 = f"{tmp2[0]}T{tmp2}:00"
    print(s)
    d = {
        'name': s[0],
        'isMicrophoneOn': s[1].lower() == 'да',
        'isVideoOn': s[2].lower() == 'да',
        'isWaitingRoomEnabled': s[3].lower() == 'да',
        'participantsCount': int(s[4]),
        'startedAt': tmp1,
        'durationx': int(s[6]),
        'sendNotificationsAt': tmp2,
        'state': 'booked'
    }
    print(d)
    return d
