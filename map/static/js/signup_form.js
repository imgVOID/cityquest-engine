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

var lastUsername = [false,false];

formValidation = {
	init: function(){
		this.$form = $('.registration-form');
		this.$firstName = this.$form.find('input[name="firstName"]');
		this.$lastName = this.$form.find('input[name="last_name"]');
		this.$username = this.$form.find('input[name="username"]');
		this.$email = this.$form.find('input[name="email"]');
		this.$password = this.$form.find('input[name="password1"]');
		this.$passwordRepeat = this.$form.find('input[name="password2"]');
		this.$passwordToggle = this.$form.find('button.toggle-visibility');
		this.$submitButton = this.$form.find('button.go');
		
		this.validatedFields = {
			firstName: false,
			lastName: false,
			username: false,
			email: false,
			password: false,
			passwordRepeat: false
		};
		
		this.bindEvents();
	},
	bindEvents: function(){
		this.$firstName.donetyping(this.validateFirstNameHandler.bind(this));
		this.$firstName.focusout(this.validateFirstNameHandler.bind(this));
		this.$lastName.donetyping(this.validateLastNameHandler.bind(this));
		this.$lastName.focusout(this.validateLastNameHandler.bind(this));
		this.$username.focusout(this.validateUsernameHandler.bind(this));
		this.$username.donetyping(this.validateUsernameHandler.bind(this));
		this.$email.focusout(this.validateEmailHandler.bind(this));
		this.$email.donetyping(this.validateEmailHandler.bind(this));
		this.$password.donetyping(this.validatePasswordHandler.bind(this));
		this.$password.focus(this.validatePasswordHandler.bind(this));
		this.$password.focusout(this.validatePasswordHandler.bind(this));
		this.$passwordRepeat.donetyping(this.validatePasswordRepeatHandler.bind(this));
		this.$passwordRepeat.focus(this.validatePasswordRepeatHandler.bind(this));
		this.$passwordRepeat.focusout(this.validatePasswordHandler.bind(this));
		this.$passwordToggle.mousedown(this.togglePasswordVisibilityHandler.bind(this));
		this.$passwordToggle.click(function(e){e.preventDefault()});
		this.$form.submit(this.submitFormHandler.bind(this));
	},
	validateFirstNameHandler: function(){
		this.validatedFields.firstName = this.validateText(this.$firstName);
	},
	validateLastNameHandler: function(){
		this.validatedFields.lastName = this.validateText(this.$lastName);
	},
	validateEmailHandler: function(){
		this.validatedFields.email = this.validateText(this.$email) && this.validateEmail(this.$email);
	},
	validateUsernameHandler: function(){
		this.validatedFields.username = this.validateUsername(this.$username);
	},
	validatePasswordHandler: function(){
		this.validatedFields.password = this.validatePassword(this.$password);
	},
	validatePasswordRepeatHandler: function(){
		this.validatedFields.passwordRepeat = this.validatePasswordRepeat(this.$passwordRepeat);
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
		this.validateFirstNameHandler();
		this.validateLastNameHandler();
		this.validateEmailHandler();
		this.validatePasswordHandler();
		this.validatePasswordRepeatHandler();
		if(this.validatedFields.firstName && this.validatedFields.lastName && this.validatedFields.email && this.validatedFields.password && this.validatedFields.passwordRepeat && this.validatedFields.username){
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
			$input.parent().find('span.label-text').append(' <small class="error"> field is empty</small>');
			return false;
		}
	},
	validateUsername: function($input){

		function display(result,content){
			content = content || '';
			if(result==false){
				$input.parent().removeClass('invalid');
				$input.parent().find('span.label-text small.error').remove();
				$input.parent().addClass('invalid');
				$input.parent().find('span.label-text').append(content);
			}else{
				$input.parent().removeClass('invalid');
				$input.parent().find('span.label-text small.error').remove();
			}
		}

		if($input.val().length > 5){
			if(lastUsername[0] !== $input.val()){
				var regEx = /^[\w.@+-]+$/;
					if(regEx.test($input.val())){
						var username = $input.val();
    					$.ajax({url: '/ajax/validate_username/', data: {'username': username}, dataType: 'json',
    						success: function (data) {
        						if (data.is_taken) {
        							display(false,' <small class="error"> already exists</small>');
									lastUsername[1] = false;
	            					return false
    	    					}else{
    	    						display(true);
        							lastUsername[1] = true;
        							return true
        						}
    						}
    					});
    					lastUsername[0] = username;
    					return lastUsername[1]
					}else{
						display(false,' <small class="error"> invalid character</small>');
						lastUsername[0] = username;
						return false
    				}
			}else{
				return lastUsername[1]
			}
		}else{
			lastUsername[0] = $input.val();
			display(false,' <small class="error"> needs 6+ symbols</small>');
			return false;
		}
	},
	validateEmail: function($input){
		var regEx = /\S+@\S+\.\S+/;
		$input.parent().removeClass('invalid');
		$input.parent().find('span.label-text small.error').remove();
    if(regEx.test($input.val())){
			return true;
		}else{
			$input.parent().addClass('invalid');
			$input.parent().find('span.label-text').append(' <small class="error"> is invalid</small>');
			return false;
		}
	},
	validatePassword: function($input){
			$input.parent().removeClass('invalid');
		$input.parent().find('span.label-text p').remove();
		$input.parent().find('span.label-text').append('<p>Password<p>');
		window.password = $input.val();
		if($input.val().length >= 8){
			return true;
		}else{
			$input.parent().addClass('invalid');
			$input.parent().find('span.label-text p').remove();
			$input.parent().find('span.label-text').append(' <p class="error"> Only 8+ symbols</p>');
			return false;
		}
	},
	validatePasswordRepeat: function($input){
		$input.parent().removeClass('invalid');
		$input.parent().find('span.label-text p').remove();
		$input.parent().find('span.label-text').append('<p>Repeat<p>');
		
		if ($input.val().length >= 8){
			if($input.val() === window.password){
				return true
			}else{
				$input.parent().addClass('invalid');
				$input.parent().find('span.label-text p').remove();
				$input.parent().find('span.label-text').append(' <p class="error">Don\'t match</p>');
				return false;
			}
		}else{
			$input.parent().addClass('invalid');
			$input.parent().find('span.label-text p').remove();
			$input.parent().find('span.label-text').append(' <p class="error"> Only 8+ symbols</p>');
			return false;
		}
	}
}.init();