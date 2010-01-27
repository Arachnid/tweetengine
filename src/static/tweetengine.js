jQuery(document).ready(function() {
    jQuery(document).ajaxError(function (event, XMLHttpRequest,
            ajaxOptions, thrownError) {
    		var msg = 'An error occurred while requesting "' + ajaxOptions.url; 
    		msg += '" Could not continue.';
    		/* alert(msg); enable for debugging */
    });	
    function counter(event) {
		var length = 140 - jQuery(this).val().length;
		if (length < 0 || length >= 139) {
			jQuery("#tweetsubmit").attr('disabled', 'disabled');
			jQuery("#tweetlabel").attr('class', 'tweet-oversize');
		};
		if (length >= 0 && length < 140) {
			jQuery("#tweetsubmit").removeAttr('disabled');
			jQuery("#tweetlabel").removeAttr('class');
		};
		jQuery("#tweetlabel").text(length);
    }
	jQuery("#tweetarea").keypress(counter);
	jQuery("#tweetarea").keyup(counter);
	jQuery("#tweetarea").keydown(counter);
	jQuery("#tweetarea").bind('input paste', counter);

	jQuery("#timeline").tabs();
	
	function fill_tweets(apicall, region) {
		var selector = "#tabs-" + region;
		if (jQuery(selector).find('.loading-timeline') == undefined) {
			return;
		}
		jQuery.getJSON("/" + account_name + "/api/"+apicall+".json", function(data){
			jQuery(selector).empty();
			if (data.length > 0) {
				jQuery.each(data, function() {
					var user = this.user;
					var is_direct = false;
					if (user == undefined) {
						user = this.sender;
						is_direct = true;
					}
					var entry = jQuery("#tweet-template").clone();
					entry.attr('id', 'status-' + this.id);
					var userurl = 'http://twitter.com/' + user.screen_name;
					entry.find(".tweet-thumb").find('a').attr('href', userurl);
					entry.find(".tweet-thumb").find('a img').attr('src', user.profile_image_url);
					entry.find(".tweet-thumb").find('a img').attr('title', user.name);
					entry.find(".tweet-user").find('a').text(user.screen_name);
					entry.find(".tweet-user").find('a').attr('href', userurl);
					entry.find(".tweet-user").find('a').attr('title', user.name);
					entry.find(".tweet-content").text(this.text);
					entry.find(".tweet-dateurl").text(this.created_at);
					entry.find(".tweet-dateurl").attr('href', userurl + "/status/" + this.id);
					if (is_direct) {
						entry.find(".tweet-source").text('direct message');
					} else {
						entry.find(".tweet-source").html(this.source);
					}
					
					jQuery(selector).append(entry);
				});
			} else {
				jQuery(selector).text('No tweets so far.')
			}
		});
	}
	fill_tweets('statuses/user_timeline', 'mytweets');
	jQuery('#timeline').bind('tabsselect', function(event, ui) {
		switch(jQuery(ui.tab).attr('href').slice(6)) 
		{
		case 'friends': 
		    fill_tweets('statuses/friends_timeline', 'friends');
		    break;
		case 'mentions':
			fill_tweets('statuses/mentions', 'mentions');
            break;
		case 'direct':
			fill_tweets('direct_messages', 'direct');
			break;
		}		
	});
});
