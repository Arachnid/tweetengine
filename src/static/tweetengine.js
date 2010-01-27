jQuery(document).ready(function() {
    jQuery(document).ajaxError(function (event, XMLHttpRequest,
            ajaxOptions, thrownError) {
    		var msg = 'An error occurred while requesting "' + ajaxOptions.url; 
    		msg += '" Could not continue.';
    		alert(msg);
    });	
	jQuery("#tweetarea").keypress(function(event){
		var length = 140 - jQuery(this).val().length;
		if (length < 0) {
			jQuery("#tweetsubmit").attr('disabled', 'disabled');
			jQuery("#tweetlabel").attr('class', 'tweet-oversize');
		};
		if (length == 0) {
			jQuery("#tweetsubmit").removeAttr('disabled');
			jQuery("#tweetlabel").removeAttr('class');
		};
		jQuery("#tweetlabel").text(length);
	});
	jQuery("#timeline").tabs();
	var mentionsurl = jQuery("#mentionsurl").attr('href');
	jQuery.getJSON("/" + account_name + "/api/statuses/mentions.json", function(data){
		jQuery("#tabs-mentions").text(data);
	})
});
