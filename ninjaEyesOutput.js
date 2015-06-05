// Wrap everything in a function
(function(i) {
	inputSplit = input.split(",")
	h = inputSplit[0] / 360
	s = inputSplit[1] / 100
	v = inputSplit[2] / 100
    
	var r, g, b;

    var i = Math.floor(h * 6);
    var f = h * 6 - i;
    var p = v * (1 - s);
    var q = v * (1 - f * s);
    var t = v * (1 - (1 - f) * s);

    switch(i % 6){
        case 0: r = v, g = t, b = p; break;
        case 1: r = q, g = v, b = p; break;
        case 2: r = p, g = v, b = t; break;
        case 3: r = p, g = q, b = v; break;
        case 4: r = t, g = p, b = v; break;
        case 5: r = v, g = p, b = q; break;
    }
	
	// return it as RRGGBB in HEX e.g. 00FF00
	r_hex = parseInt(r * 255).toString(16);
	g_hex = parseInt(g * 255).toString(16);
	b_hex = parseInt(b * 255).toString(16);
	
	// if the number is < 0xF then we have to pad it with a zero
	if(r_hex.length == 1)
		r_hex = '0' + r_hex;
	if(g_hex.length == 1)
		g_hex = '0' + g_hex;
	if(b_hex.length == 1)
		b_hex = '0' + b_hex;
	
    return r_hex.concat(g_hex,b_hex).toUpperCase();
})(input)
// input variable contains data passed by openhab