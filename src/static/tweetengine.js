jQuery(document).ready(function() {
    url_re = /\b(https?|ftp|file):\/\/[-A-Z0-9+&@#/%?=~_|!:,.;]*[-A-Z0-9+&@#/%=~_|]/ig;
    username_re = /@([A-Z0-9_]+)/ig;
    function linkify(text) {
        text = text.replace(url_re, "<a href=\"$&\">$&</a>");
        text = text.replace(username_re, "<a href=\"http://twitter.com/$1\">@$1</a>");
        return text;
    }

    var tweetarea = jQuery("#tweetarea");
    jQuery(document).ajaxError(function (event, XMLHttpRequest,
            ajaxOptions, thrownError) {
    		var msg = 'An error occurred while requesting "' + ajaxOptions.url; 
    		msg += '" Could not continue.';
    		/* alert(msg); enable for debugging */
    });	
    function counter(event) {
		var length = 140 - tweetarea.val().length;
		if (length <= 0 || length >= 139) {
			jQuery("#tweetsubmit").attr('disabled', 'disabled');
			jQuery("#tweetlabel").attr('class', 'tweet-oversize');
		};
		if (length > 0 && length < 140) {
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
	
	function fill_tweets(region) {
		var selector = "#tabs-" + region;
		if (jQuery(selector).find('.loading-timeline') == undefined) {
			return;
		}
		jQuery.getJSON("/" + account_name + "/api/"+region+".json", function(data){
			jQuery(selector).empty();
			if (data.length > 0) {
				var orderedlist = jQuery("#tweet-template").clone();
				orderedlist.empty();
				orderedlist.attr('id', 'orderedlist'+region);
				jQuery(selector).append(orderedlist);
				jQuery.each(data, function() {
					var user = this.user;
					var is_direct = false;
					if (user == undefined) {
						user = this.sender;
						is_direct = true;
					}
					var entry = jQuery("#tweet-template li").clone();
                    entry.data("status_id", this.id);
					entry.attr('id', 'status-' + this.id);
					var userurl = 'http://twitter.com/' + user.screen_name;
					entry.find(".tweet-thumb").find('a').attr('href', userurl);
					entry.find(".tweet-thumb").find('a img').attr('src', user.profile_image_url);
					entry.find(".tweet-thumb").find('a img').attr('title', user.name);
					entry.find(".tweet-user").find('a').text(user.screen_name);
					entry.find(".tweet-user").find('a').attr('href', userurl);
					entry.find(".tweet-user").find('a').attr('title', user.name);
					entry.find(".tweet-content").html(linkify(this.text));
					entry.find(".tweet-dateurl").text(this.created_at);
					entry.find(".tweet-dateurl").attr('href', userurl + "/status/" + this.id);
					if (is_direct) {
						entry.find(".tweet-source").text('direct message');
					} else {
						entry.find(".tweet-source").html(this.source);
					}					
					if (region!='mytweets') {
						entry.find(".tweet-reply").unbind("click").click(function() {
                            var tweet = jQuery(this).parents("li");
                            var user = tweet.find(".tweet-user a").text();
                            tweetarea.text("@" + user + " ");
                            tweetarea.focus();
                            counter();
                            jQuery("#in-reply-to").attr("value", tweet.data("status_id"));
	                    });
	                    entry.find(".tweet-retweet").unbind("click").click(function() {
                            var tweet = jQuery(this).parents("li");
                            var user = tweet.find(".tweet-user a").text();
                            var text = tweet.find(".tweet-content").text();
                            tweetarea.text("RT @" + user + " " + text);
                            tweetarea.focus();
                            counter();
	                    });
                        entry.hover(function() {
                            $(this).find(".tweet-actions").css("display", "block");
                        }, function() {
                            $(this).find(".tweet-actions").css("display", "none");
                        });
                    } else {
						jQuery(entry).find('.tweet-actions').remove();
					}
					orderedlist.append(entry);
				});
			} else {
				jQuery(selector).text('No tweets so far.')
			}
		});
	}
	fill_tweets('mytweets');
	jQuery('#timeline').bind('tabsselect', function(event, ui) {
		switch(jQuery(ui.tab).attr('href').slice(6)) 
		{
		case 'friends': 
		    fill_tweets('friends');
		    break;
		case 'mentions':
			fill_tweets('mentions');
            break;
		case 'direct':
			fill_tweets('direct');
			break;
		}		
	});                       
    jQuery('.datestamp').dateEntry({dateFormat: 'dmy/',
		                   spinnerImage: '/static/dateentry/spinnerDefault.png',
                           spinnerBigImage: '/static/dateentry/spinnerDefaultBig.png'});
    jQuery('.timestamp').timeEntry({show24Hours: true, timeSteps: [1,5,60], initialField: 1,
		                   spinnerImage: '/static/dateentry/spinnerDefault.png',
                           spinnerBigImage: '/static/dateentry/spinnerDefaultBig.png'});

    var now = new Date();
    jQuery("#tweetbox .datestamp").dateEntry("setDate", now);
    jQuery("#tweetbox .timestamp").timeEntry("setTime", now);
    jQuery("#tweetbox .datestamp, #tweetbox .timestamp").focus(function() {
        jQuery("#whensched").attr("checked", "checked");
    });
});
