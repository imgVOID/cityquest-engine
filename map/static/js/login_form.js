//https://codepen.io/tylernj42/pen/BoxzaQ
//https://www.tramptravel.ro/uploads/images/ucraina1.jpg
(function($){
    $.fn.extend({
        donetyping: function(callback,timeout){
            timeout = timeout || 500;
            var timeoutReference,
                doneTyping = function(el){
                    if (!timeoutReference) return;
                    timeoutReference = null;
                    callback.call(el);
                };
            return this.each(function(i,el){
                var $el = $(el);
                $el.is(':input') && $el.on('keyup keypress',function(e){
                    if (e.type=='keyup' && e.keyCode!=8) return;
                    if (timeoutReference) clearTimeout(timeoutReference);
                    timeoutReference = setTimeout(function(){
                        doneTyping(el);
                    }, timeout);
                }).on('blur',function(){
                    doneTyping(el);
                });
            });
        }
    });
})(jQuery);

formValidation = {
	init: function(){
		this.$form = $('.registration-form');
		this.$username = this.$form.find('input[name="username"]');
		this.$password = this.$form.find('input[name="password"]');
		this.$passwordToggle = this.$form.find('button.toggle-visibility');
		this.$submitButton = this.$form.find('button.go');
		
		this.validatedFields = {
			username: false,
			password: false
		};
		
		this.bindEvents();
	},
	bindEvents: function(){
		this.$username.donetyping(this.validateUsernameHandler.bind(this));
		this.$password.donetyping(this.validatePasswordHandler.bind(this));
		this.$passwordToggle.mousedown(this.togglePasswordVisibilityHandler.bind(this));
		this.$passwordToggle.click(function(e){e.preventDefault()});
		this.$form.submit(this.submitFormHandler.bind(this));
	},
	validateUsernameHandler: function(){
		this.validatedFields.username = this.validateText(this.$username);
	},
	validatePasswordHandler: function(){
		this.validatedFields.password = this.validateText(this.$password) && this.validatePassword(this.$password);
	},
	togglePasswordVisibilityHandler: function(){
		var html = '<input type="text" value="'+this.$password.val()+'">';
		var $passwordParent = this.$password.parent()
		var saved$password = this.$password.detach();
		$passwordParent.append(html);
		this.$passwordToggle.find('span').removeClass('glyphicon-eye-close').addClass('glyphicon-eye-open');
		this.$passwordToggle.one('mouseup mouseleave', (function(){
			$passwordParent.find('input').remove();
			$passwordParent.append(saved$password);
			this.$passwordToggle.find('span').removeClass('glyphicon-eye-open').addClass('glyphicon-eye-close');
		}).bind(this));
	},
	submitFormHandler: function(e){
		this.validateUsernameHandler();
		this.validatePasswordHandler();
		if(this.validatedFields.username && this.validatedFields.password){
			this.$submitButton.addClass('loading').html('<span class="loading-spinner"></span>')
		}else{
		    e.preventDefault();
			this.$submitButton.text('Fix me!');
			setTimeout((function(){
				if(this.$submitButton.text() == 'Fix me!'){
					this.$submitButton.text('Sign in');
				}
			}).bind(this), 3000)
		}
	},
	
	validateText: function($input){
		$input.parent().removeClass('invalid');
		$input.parent().find('span.label-text small.error').remove();
		if($input.val() != ''){
			return true;
		}else{
			$input.parent().addClass('invalid');
			$input.parent().find('span.label-text').append(' <small class="error"> is empty</small>');
			return false;
		}
	},
	validatePassword: function($input){
			$input.parent().removeClass('invalid');
		$input.parent().find('span.label-text small.error').remove();
		if($input.val().length >= 8){
			return true;
		}else{
			$input.parent().addClass('invalid');
			$input.parent().find('span.label-text').append(' <small class="error"> must have 8+ characters</small>');
			return false;
		}
	}
}.init();