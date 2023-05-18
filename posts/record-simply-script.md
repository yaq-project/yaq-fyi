---
title: Recording Data Simply
id: record-simply-script
date: 2023-05-18
authors: Blaise Thompson
---

When you're trying something new, it can be daunting to develop a fully-featured framework for hardware orchestration and data recording.
Luckily it's pretty easy to "start small" using yaq.

The following is a script developed by the Krishna Group for simply dumping hardware state periodically to an ASCII data file.
The Krishna Group uses yaqc-qtpy to provide a generic "interactive" interface for controlling hardware while this script runs in the terminal, recording data.

This script is pretty neat because it tries to read from the different daemons and come up with appropriate headers based on the traits they support.
For most daemons, you should just be able to modify the ports list and run the script.
Hope this blog post inspires further creativity in writing small scripts using yaq!

    import yaqc
    import tidy_headers
    import numpy as np
    import time
    from datetime import datetime, timezone

    poll_period = 10  # seconds between each record

    ports = [38000,
             38001,
             38002,
             38003,
             38004,
             38005,
             38100,
             38200,
             38201,
             38300]


    # connect to all peripherals ---------------------------------------------------------------------

    clients = []

    for port in ports:
        clients.append(yaqc.Client(port))

    # create file, header ----------------------------------------------------------------------------

    local_time = datetime.now(timezone.utc).astimezone()

    header = dict()
    header ["timestamp"] = local_time.isoformat()

    # get column information from clients
    columns = ["timestamp"]
    for client in clients:
        if "has-position" in client.traits:
            columns.append(f"{client.id()['name']}_destination")
            columns.append(f"{client.id()['name']}_position")
        elif "is-sensor" in client.traits:
            for channel in client.get_channel_names():
                columns.append(f"{client.id()['name']}_{channel}")
    header["columns"] = columns
    header["objective"] = "Wacker Reaction over CuPdNa-CBV400 calcined catalyst (Pd nitrate)"
    header["reaction"] = "Catalyst: 51.2 mg of CuPdNa-CBV400 calcined sieved"
    header["test"] = ["this", "is", "a", "list"]

    filename = local_time.strftime("%Y%m%d_%H%M%S.txt")
    tidy_headers.write(filename, header)

    # record data ------------------------------------------------------------------------------------

    with open(filename, "a") as f:
        while True:
            last_record = time.time()
            row = [last_record]
            for client in clients:
                if "has-position" in client.traits:
                    row.append(client.get_destination())
                    row.append(client.get_position())
                elif "is-sensor" in client.traits:
                    channels = client.get_channel_names()
                    measurement = client.get_measured()
                    for channel in channels:
                        row.append(measurement[channel])
            line = "\t".join([str(i) for i in row]) + "\n"
            print(line)
            f.write(line)
            f.flush()
            while (time.time() - last_record) < poll_period:
                time.sleep(0)