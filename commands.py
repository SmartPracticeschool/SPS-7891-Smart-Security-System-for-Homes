def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data)
    print(cmd.data['command'])

    if (cmd.data['command'] == "open"):
        print("door open")

    if (cmd.data['command'] == "close"):
        print("door close")

    if (cmd.data['command'] == "lighton"):
        print("light on")

    if (cmd.data['command'] == "lightoff"):
        print("light off")

    if (cmd.data['command'] == "fanon"):
        print("fan on")

    if (cmd.data['command'] == "fanoff"):
        print("fan off")