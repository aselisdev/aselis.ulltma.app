function showhref(x, kw) {
    dest = window.location.href;
	url = document.getElementById('link_'+x).href;

	data = {link:url};
	$.get(dest, data, function(data, status){
		console.log(status);
	});
}