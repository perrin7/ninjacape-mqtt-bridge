# ninjacape-mqtt-bridge
<html>
<h2>Python script for grabbing JSON data over serial from the NinjaCape and publishing it as MQTT messages</h2>

You need to have an MQTT broker installed, such as http://mosquitto.org/

<h3>MQTT messages are structured as follows:</h3>
<ul>
<li>Messages received on 433Mhz as published to:
<br>/ninjaCape/input/<i>DeviceID</i>
<br>payload: <i>DeviceData</i>
</li>
<li>
Messages to be sent out on 433Mhz should be pushlished to:
<br>/ninjaCape/output/<i>DeviceID</i>
<br>payload: <i>DeviceData</i>
</li>
<li>The script subscribes to all updates on /ninjaCape/output/#</li>
</ul>
</html>
