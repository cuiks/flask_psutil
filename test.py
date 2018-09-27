# -*- coding: utf-8 -*-
import psutil
alls= psutil.disk_partitions()
for all in alls:
    print(psutil.disk_usage(all.device))