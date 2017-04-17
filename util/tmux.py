class TmuxHandler:
    @staticmethod
    def new_tmux_cmd(session, name, cmd):
        if isinstance(cmd, (list, tuple)):
            cmd = " ".join(str(v) for v in cmd)
        return name, "tmux send-keys -t {}:{} '{}' Enter".format(session, name, cmd)

    @staticmethod
    def create_tmux_commands(session,  usercmd):
        cmds_map = [TmuxHandler.new_tmux_cmd(session, "usercmd", [usercmd])]
        
        windows = [v[0] for v in cmds_map]

        cmds = [
            #"mkdir -p {}".format(logdir),
            "tmux kill-session -t {}".format(session),
            "tmux new-session -s {} -n {} -d".format(session, windows[0]),
        ]
        for w in windows[1:]:
            cmds += ["tmux new-window -t {} -n {}".format(session, w)]
        cmds += ["sleep 1"]
        for window, cmd in cmds_map:
            cmds += [cmd]

        return cmds
