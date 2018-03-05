var safetyInsurance = JSON.parse($('#safety-insurance').val());
var travelInsurance = JSON.parse($('#travel-insurance').val());
var userAgreement = HEINIUAGREEMENT;

var STATIC = {

	// 判断手机类型
	isIOS: function() {
      var agentStr = (navigator.userAgent).toLowerCase();
      var flag = agentStr.indexOf('iphone');
      if (flag > -1) {
        return true;
      } else {
        return false;
      }
    },

	// 保存js的DOM操作状态
	saveDomStatus: function () {
		if ($.cookie('inputBox') == 'yes') {
			$.cookie('inputBox', 'no', { path: '/' });
			$('#birth, #mobile, #have-credit-card-box').css('display', 'block');
		} else {
			$('#birth, #mobile, #have-credit-card-box').css('display', 'none');
		}
	},

    // 广播滚动特效
    broadcastScroll: function (broadcastBoxId) {
        var broadcastStr = broadcastBoxId.html();
        var count = 0;
        broadcastBoxId.html('').html(broadcastStr + broadcastStr);
        var h = $('li', broadcastBoxId).eq(0).height();
        var len = $('li', broadcastBoxId).length;
        broadcastBoxId.height(h * len);

        setInterval(function () {
            if (count >= len / 2) {
                count = 0;
                broadcastBoxId.css('top', 0);
            }
            count++;
            broadcastBoxId.animate({ top: -(h * count) + 'px' }, 'slow');
        }, 3000);
    },

    // 成功提交函数
    _submitSucess: function (url) {
    	var self = this;
	    MODALCAPTCHA._close();
    	$('#mask, #success-box').css('display', 'block');
    	setTimeout(function(){
	    	$('#mask').height($(document).height());
	    	$('#success-box').css('top', 100 + $(window).scrollTop());
    	}, 0);
	    setTimeout(function(){
          window.location.href = url;
	    }, 2200);
    },

	// 验证验证码
	_validateCaptcha: function (options) {
		var self = this;
	    $.ajax({
	        type: 'get',
	        async: false,
	        url: $('#get-verify-interface').val(),
	        data: options.req,
	        success: function(response){
	          if(response.error_code != 0)
	          {
	            options.token.val('');
	            salert(response.error_msg || '验证码输入错误');
	          }
	          else
	          {
	            options.token.val(response.token);
	            setTimeout(function(){
	            	self._submitSucess(response.page_url);
	            }, 200);
	          }
	        },
	        error: function() {
	          salert('服务器繁忙，请稍后重试...');
	        }
	    });
	  },

    // 倒计时
    _timer: null,
	_times: 60,
	_cutdown: function (sendId) {
	   var self = this;
	   clearInterval(self._timer);
	   self._times = 60;
	   sendId.attr('disabled',true).text(self._times + "秒后重试");

	   self._timer = setInterval(function () {
	     self._times --;
	     sendId.text(self._times + "秒后重试");
	     if(self._times <= 0){
	       sendId.removeAttr('disabled');
	       sendId.text("获取验证码");
	       clearInterval(self._timer);
	       self._times = 60;
	     }

	   },1000);
	},

    // 获取验证码
    getCaptcha: function (options) {
	    var self = this;
	    $.ajax({
	        type: 'get',
	        async: false,
	        url: '/gen/phone_hnyq_captcha',
	        data: options.req,
	        success: function(response){
	          if(response.error_code === 0)
	          {
	            self._cutdown(options.sendId);
	          }
	          else
	          {
	            salert(response.error_msg);
	          }
	        },
	        error: function(){
	          salert('网络繁忙，请稍后重试...');
	        }
	    });
	},

	// 模态框
	modalHtml: function (title, content) {
		var str = '';
		$('strong', '#modal-box h3').text(title);
		$.each(content, function(index, item){
			str += '<p>' + item + '</p>';
		});
		$('#modal-msg-box').html('').html(str);
		setTimeout(function(){
			$('#mask, #modal-box').css('display', 'block');
			$('#mask').height($(window).height() > $(document).height()
												 ? $(window).height()
												 : $(document).height());
		}, 0);
	}

};

// 验证码弹窗初始化
MODALCAPTCHA._init($('#static-host').val(), $('#captcha'));

// 保存js的DOM操作状态
if (!STATIC.isIOS()) {
	var showInput = STATIC.saveDomStatus();
}

// 广播滚动特效
var broadcastBoxId = $('ul', '#broadcast-box');
STATIC.broadcastScroll(broadcastBoxId);

// 输入金额
var regNumber = /^\d+(\.\d+)?$/;
$('input[name="amount"]').on('blur', function(){
	var self = $(this);
	if (self.val() === '') {
		salert('借款金额不能为空');
	} else if (regNumber.test(self.val())) {
		var value = Number(self.val());
		if (value < 500) {
			self.val(500);
			salert('最少借500元');
		} else if (value > 300000) {
			self.val(300000)
			salert('最多借30万元');
		} else if (isNaN(value)) {
			salert('借款金额格式错误');
		}
	} else {
		salert('借款金额只能为阿拉伯数字');
	}
});


// 选择性别
$('input[name="sex"]').on('change', function(){
	$('#birth, #mobile, #have-credit-card-box').css('display', 'block');
});

// 选择复选框
$('#agree-btn').on('click', function(){
	if ($(this).is(':checked')) {
		$('input[name="agree"]').val('Y');
	} else {
		$('input[name="agree"]').val('N');
	};
});

// 提交表单
$('#submit-btn').on('click', function(e){
	var valid = true;
	if (valid) {
		if (!regNumber.test($('input[name="amount"]').val())) {
			valid = false;
			salert('请输入正确的借款金额');
			return false;
		}
		if (!REG._reg('name').test($('input[name="name"]').val())) {
			valid = false;
			salert(REG._error('name'));
			return false;
		}
	}

	if (valid) {
		var sexFlag = false;
		$('input[name="sex"]').each(function(index, item){
			if ($(item).is(':checked')) {
				sexFlag = true
			}
		});
		if (!sexFlag) {
	      valid = false;
	      salert('请选择性别');
	    }
	}

	if (valid) {
		var creditFlag = false;
		$('input[name="credit"]').each(function(index, item){
			if ($(item).is(':checked')) {
				creditFlag = true
			}
		});
		if (!creditFlag) {
	      valid = false;
	      salert('请选择是否拥有信用卡');
	    }
	}

	if (valid) {
		if (!REG._reg('birth').test($('input[name="birth"]').val())) {
			valid = false;
			salert(REG._error('birth'));
			return false;
		}
		if (!REG._reg('mobile').test($('input[name="mobile"]').val())) {
			valid = false;
			salert(REG._error('mobile'));
			return false;
		}
	}

	if (valid) {
		if ($('#agree-btn').is(':checked')) {
			$('input[name="agree"]').val('Y');
		} else {
			$('input[name="agree"]').val('N');
		};
	}

	if (valid) {
		$.ajax({
			type: 'get',
			url: $('#get-check-user-interface').val(),
			data: UTIL._formatData($('#form-box')),
			success: function (response) {
				if (response.status === 0) {
					var getOptions = {
						req: {
							r: $('#random').val(),
							phone: $('input[name="mobile"]').val()
						},
						sendId: MODALCAPTCHA._sendId
					};
					STATIC.getCaptcha(getOptions);
					MODALCAPTCHA._sendId.on('click', function(){
						if (!$(this).attr('disabled')) {
							STATIC.getCaptcha(getOptions);
						}
					});
					MODALCAPTCHA._show($('input[name="mobile"]').val(), function(){
		          	var validOptions = {
						req: {
							phone: $('input[name="mobile"]').val(),
							captcha: $('input[name="captcha"]').val()
						},
						token: $('#token')
					  };
		              STATIC._validateCaptcha(validOptions);
			        });
				} else if (response.status === 1) {
					window.location.href = response.page_url;
				} else {
					salert(response.error_msg);
				}
			},
			error: function () {
				salert('网络繁忙，请稍后重试...');
			}
		});
	}

	if(!valid) {
        e.preventDefault();
        return false;
    }
});

// 弹窗
$('a', '.agree-box').on('click', function(){
	var self = $(this);
	if (self.text() == '账户资金安全险') {
		STATIC.modalHtml(self.text(), safetyInsurance);
	} else if (self.text() == '出行险') {
		STATIC.modalHtml(self.text(), travelInsurance);
	} else if (self.text() == '用户协议') {
		STATIC.modalHtml(self.text(), userAgreement);
	}
});

$('span', '#modal-box h3').on('click', function(){
	$('#mask, #modal-box').css('display', 'none');
});













