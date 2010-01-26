
jQuery(document).ready(function() {
	jQuery("#tweetarea").keyup(function(event){
		var length = 140 - jQuery(this).val().length;
		if (length < 0) {
			length = 0;
			jQuery("#tweetarea").val(
					jQuery("#tweetarea").val().slice(0, 140)
			);
		};
		jQuery("#tweetlabel").text(length);
	});
});