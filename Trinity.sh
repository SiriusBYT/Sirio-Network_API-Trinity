clear
echo [Trinity API] Script Started
cd /System/Services/Trinity-API
while :
do
	echo [Trinity API] Info: Launching the Trinity API...
	python3 Trinity.py
	echo [Trinity API] WARNING: Server has crashed or shutted down ! Restarting server automatically in 10 seconds.
	sleep 10
done
echo [Trinity API] Goodbye.
