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
    def get_panel_from_sess(self,sess):
        window = sess.attached_window
        pane = window.list_panes()[0]
        return pane

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
                
    def close_sess_by_filter(self,include_names=[],exclude_names=[],start_sess_id=0):
        for idx, sess in enumerate(self.list_serssions()):
            string_s = str(sess)
            print(string_s)

            exclude_flag=False
            for ex_e in exclude_names:
                if ex_e in string_s:
                    exclude_flag=True
                    break
                    
            if exclude_flag==True:
                continue
             
            inc_flag=True   
            for in_e in include_names:
                if in_e in string_s:
                    inc_flag=True
                    break
                else:
                    inc_flag=False
            
            if inc_flag == False:
                continue
                
                      
            my_id = int(string_s.split("s_")[-1].replace(")",""))
            if my_id >= start_sess_id:
                print(sess,my_id,start_sess_id, "can be killed")
                sess.attached_window.kill_window()