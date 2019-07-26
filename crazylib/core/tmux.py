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

