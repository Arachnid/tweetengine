jQuery(document).ready(function() {
	jQuery("#tweetarea").keyup(function(event){
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
});