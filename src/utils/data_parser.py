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
