// Wrap everything in a function
(function(i) {
    var r = parseInt(input.substring(-1,2),16)
	var g = parseInt(input.substring(1,4),16)
	var b = parseInt(input.substring(3,6),16)

	// http://axonflux.com/handy-rgb-to-hsl-and-rgb-to-hsv-color-model-c
    r = r/255, g = g/255, b = b/255;
    var max = Math.max(r, g, b), min = Math.min(r, g, b);
    var h, s, v = max;

    var d = max - min;
    s = max == 0 ? 0 : d / max;

    if(max == min){
        h = 0; // achromatic
    }else{
        switch(max){
            case r: h = (g - b) / d + (g < b ? 6 : 0); break;
            case g: h = (b - r) / d + 2; break;
            case b: h = (r - g) / d + 4; break;
        }
        h /= 6;
    }

	// make it degrees and percent and return as string with CSV
	h *= 360
	s *= 100
	v *= 100
	
	// protect against quantisation errors
	if(h>=360)
		h = 360;
	if(s>=100) 
		s = 100;
	if(v>=100) 
		v = 100;
	
	return h.toString().concat(",",s,",",v)
	//return "120,100,100"
})(input)
// input variable contains data passed by openhab