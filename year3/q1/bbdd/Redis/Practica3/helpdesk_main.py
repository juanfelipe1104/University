import helpdesk

print("Petición de ayuda:")
helpdesk.request_help("b", priority=10)
helpdesk.request_help("a", priority=11)
helpdesk.request_help("x", priority=12)
helpdesk.request_help("y", priority=22)
helpdesk.request_help("z", priority=21)
helpdesk.request_help("k", priority=9)
helpdesk.request_help("l", priority=3)
helpdesk.request_help("m", priority=8)
helpdesk.request_help("n", priority=24)
helpdesk.request_help("o", priority=15)
helpdesk.request_help("p", priority=16)

uid = -1

while uid is not None:
    uid = helpdesk.attend_next_help(timeout=5)
    if uid is not None:
        print("Atendido usuario:", uid)