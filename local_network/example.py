from local_network import Router, Server, Data

router = Router()
sv_from, sv_from2 = Server(), Server()
router.link(sv_from)
router.link(sv_from2)
router.link(Server())
router.link(Server())
sv_to = Server()
router.link(sv_to)
sv_from.send_data(Data("Hello from sv1", sv_to.get_ip()))
sv_from2.send_data(Data("Hello from sv2", sv_to.get_ip()))
sv_to.send_data(Data("Hello from sv_to", sv_from.get_ip()))
router.send_data()
msg_lst_from = sv_from.get_data()
msg_lst_to = sv_to.get_data()
unpack = lambda msg_lst: [str(msg) for msg in msg_lst]
print(unpack(msg_lst_from), unpack(msg_lst_to), sep="\n")
