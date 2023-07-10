# steam-price-checker


Useful app that can help people that invested in items on steam market and are too lazy to manually check their prices.

# Available commands:
For main version (prefix=.):<br>
start = to start loop that will check prices every 5 minutes and notify you when price hit price you write in sellat<br>
prices = to get prices of your items, how many you bought them and for how much<br>
status = to check if loop working (loop is buggy so use it sometimes)<br>
ids = to check id's of yours items<br>
sellat (ID) (FLOAT) = with this you can edit sellat without editing json file<br>
dev = for tests <br>

For cmdVersion:<br>
Same commands but without start and status because this version doesn't have loop<br>

You need to create *config.json* file and edit it like this!
<br>
<pre>{
	"apiIDs" : {
		"steam" : "steam api ID",
		"discord" : "discord api ID"
	}
}</pre>