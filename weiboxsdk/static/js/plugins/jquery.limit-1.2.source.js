(function($){ 
     $.fn.extend({  
         limit: function(limit,element,callback) {
			
			var interval, f;
			var self = $(this);
					
			$(this).focus(function(){
				interval = window.setInterval(substring,100);
			});
			
			$(this).blur(function(){
				clearInterval(interval);
				substring();
			});
			
			substringFunction = "function substring(){ var val = $(self).val();var length = val.length;if(length > limit){$(self).val($(self).val().substring(0,limit));}";
			if(typeof element != 'undefined')
				substringFunction += "if($(element).html() != limit-length){$(element).html((limit-length<=0)?'0':limit-length);}"
			
			if(callback)
				substringFunction+=callback;
							
			substringFunction += "}";
			
			eval(substringFunction);
			
			
			
			substring();
			
        } 
    }); 
})(jQuery);
