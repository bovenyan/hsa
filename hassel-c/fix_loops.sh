#!/bin/sh
./tfmod.py -p tfs/stanford bbrb_rtr --rm 122,118,113,103 --add 103,113,118,122 "ip_dst=171.67.0.75/32;in_ports=^;new_vlan=0;out_ports=^te7/1:ip_dst=171.67.0.171/32;in_ports=^;new_vlan=0;out_ports=^te7/1:ip_dst=171.67.0.203/32;in_ports=^;new_vlan=0;out_ports=^te7/1:ip_dst=171.67.0.235/32;in_ports=^;new_vlan=0;out_ports=^te7/1"
./tfmod.py -p tfs/stanford coza_rtr --add 370 "ip_dst=171.66.255.128/26;in_ports=^;new_vlan=11;out_ports=^te3/1"
./tfmod.py -p tfs/stanford sozb_rtr --add 282 "ip_dst=171.66.255.128/26;in_ports=^;new_vlan=0;out_ports=^te2/1"
./tfmod.py -p tfs/stanford soza_rtr --add 462 "ip_dst=171.66.255.128/26;in_ports=^;new_vlan=0;out_ports=^te3/1"
./tfmod.py -p tfs/stanford cozb_rtr --add 297 "ip_dst=171.66.255.128/26;in_ports=^;new_vlan=0;out_ports=^te2/1"
./tfmod.py -p tfs/stanford bbra_rtr --rm 460 --add 460 "ip_dst=171.67.4.128/26;in_ports=^;new_vlan=0;out_ports=^te1/3"
./tfmod.py -p tfs/stanford yoza_rtr --rm 1888 --add 1888 "ip_dst=172.26.4.152/29;in_ports=^;new_vlan=208;out_ports=^gi2/3,^gi2/4,^gi2/13,^gi2/16,^gi3/3,^gi3/4,^fa4/42,^fa4/44,^te7/2"

./gen stanford
