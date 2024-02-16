#!/bin/bash

# Log CPU usage
cpu_log="cpu.log"
echo "Logging CPU usage to $cpu_log"
echo "--- CPU Usage Log ---" > $cpu_log

# Log Memory usage
memory_log="memory.log"
echo "Logging memory usage to $memory_log"
echo "--- Memory Usage Log ---" > $memory_log

# Log Disk I/O
disk_io_log="disk_io.log"
echo "Logging disk I/O to $disk_io_log"
echo "--- Disk I/O Log ---" > $disk_io_log

# Log Network usage
network_log="network.log"
echo "Logging network usage to $network_log"
echo "--- Network Usage Log ---" > $network_log

# Logging interval in seconds
interval=5

while true; do
    # CPU Usage
    echo "$(date) - CPU Usage:" >> $cpu_log
    top -l 1 | grep "CPU usage" >> $cpu_log

    # Memory Usage
    echo "$(date) - Memory Usage:" >> $memory_log
    vm_stat | perl -ne '/page size of (\d+)/ and $size=$1; /Pages free:\s+(\d+)/ and printf("Free RAM: %.2f MiB\n", $1 * $size / 1048576);' >> $memory_log

    # Disk I/O
    echo "$(date) - Disk I/O:" >> $disk_io_log
    iostat -d -c 2 | tail -n +3 >> $disk_io_log

    # Network Usage - simplistic approach using netstat
    # Note: For detailed monitoring, a more complex approach is required
    echo "$(date) - Network Usage:" >> $network_log
    netstat -ib | awk '/en0/ {print $7, $10}' | while read in_bytes out_bytes; do
        echo "Bytes In: $in_bytes, Bytes Out: $out_bytes"
    done >> $network_log

    sleep $interval
done
