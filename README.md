# ninjacape-mqtt-bridge
<html>
<h2>Python script for grabbing JSON data over serial from the NinjaCape and publishing it as MQTT messages</h2>

You need to have an MQTT broker installed, such as http://mosquitto.org/

<br><b><a href="https://github.com/perrin7/ninjacape-mqtt-bridge/wiki">See the wiki for more information</a></b>

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

<h2>TODO List</h2>
<ul><li>Make it daemon-ised.  At the moment I'm just running it in a 'screen' instance.  </li>
<li>Catch invalid JSON messages and throw an error, instead of just ignoring it.</li>
<li><a href="https://discuss.ninjablocks.com/t/openhab-vs-open-source-sphere/3680/55">Update the MQTT message to have an additional layer for the 'gid' instead of assuming its zero. </a></li>
<li>Make the MQTT topic configurable, some brokers (i.e. eventghost) require a <i>leading</i> slash to work</li>
</ul>
</html>
