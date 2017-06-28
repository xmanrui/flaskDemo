ps -elf|grep 'python tmp'|grep -v grep|awk '{print $4}'|xargs kill -9
