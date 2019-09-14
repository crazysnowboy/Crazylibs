import numpy as np

class TmuxManager():
    def __init__(self):
        import libtmux
        self.server = libtmux.Server()
    def list_serssions(self):
        try:
            sess_list = self.server.list_sessions()
            return sess_list
        except Exception:
            return []

    def kill_all_sessions(self):
        try:
            for sess in self.list_serssions():
                window = sess.attached_window
                window.kill_window()

            return True
        except Exception:
            return False

    def create_session(self,session_name="CrazySession",win_name="CrazyWin"):
        sess  = self.server.new_session(session_name=session_name,
                                window_name=win_name)

        window = sess.attached_window
        pane = window.list_panes()[0]
        return sess,pane

    def clear_sess(self,ignore_ids=[]):
        for idx, sess in enumerate(self.list_serssions()):
            string_s = str(sess)
            sess_id = int(string_s.split("$")[-1].split(" ")[0])
            print("sess_id =", sess_id)
            if sess_id not in ignore_ids:
                print(sess, "can be killed")
                sess.attached_window.kill_window()
    def close_sess_by_name(self,sess_name):
        for idx, sess in enumerate(self.list_serssions()):
            string_s = str(sess)
            if sess_name in string_s:
                print(sess, "can be killed")
                sess.attached_window.kill_window()