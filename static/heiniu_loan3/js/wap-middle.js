var safetyInsurance = JSON.parse($('#safety-insurance').val());
var travelInsurance = JSON.parse($('#travel-insurance').val());

var STATIC = {
	// 保存js的DOM操作状态
	saveDomStatus: function () {
		if ($.cookie('question') == 'yes') {
			$.cookie('question') == 'no'
			$('#form-salary-box').css('display', 'block');
		} else {
			$('#form-salary-box').css('display', 'none');
		}
	},

	// 创建动态问卷
	createHtml: function (content) {
		var parentHtml = '';
		$.each(content, function(index, item){
			var $title = item.title;
			var $name = item.name;
			var $options = item.options;
			var childHtml = '';
			$.each($options, function(_index, _item){
				childHtml += '<input id="'+ $name + (_index+1) +'" type="radio"' +
				               'name="'+ $name +'" value="'+ _item.value +'">' +
		                     '<label for="'+ $name + (_index+1) +'">'+ _item.text +'</label>';
			});
			parentHtml += '<div class="form-item-box clearfix">' +
				              '<div class="item-name-box fl">' + $title + '</div>' +
				              '<div class="item-radio-box fl">' + childHtml + '</div>' +
				          '</div>';
		});
		$('#form-salary-box').html('').html(parentHtml);
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

STATIC.saveDomStatus();

// 月收入+工作时间问卷
var office = [
	{
		title: '工资发放',
		name: 'way',
		options: [
			{ text: '银行转账', value: 'A' },
			{ text: '现金发放', value: 'B' }
		]
	},
	{
		title: '月收入',
		name: 'salary',
		options: [
			{ text: '5千以下', value: 'A' },
			{ text: '5千-1万', value: 'B' },
			{ text: '1万以上', value: 'C' }
		]
	},
	{
		title: '公积金',
		name: 'fund',
		options: [
			{ text: '无公积金', value: 'A' },
			{ text: '1年以内', value: 'B' },
			{ text: '1年以上', value: 'C' }
		]
	},
	{
		title: '工作时间',
		name: 'experience',
		options: [
			{ text: '6个月内', value: 'A' },
			{ text: '12个月内', value: 'B' },
			{ text: '1年以上', value: 'C' }
		]
	}
];
var civil = [
	{
		title: '月收入',
		name: 'salary',
		options: [
			{ text: '5千以下', value: 'A' },
			{ text: '5千-1万', value: 'B' },
			{ text: '1万以上', value: 'C' }
		]
	},
	{
		title: '工作时间',
		name: 'experience',
		options: [
			{ text: '6个月内', value: 'A' },
			{ text: '12个月内', value: 'B' },
			{ text: '1年以上', value: 'C' }
		]
	}
];
var private = [
	{
		title: '月收入',
		name: 'salary',
		options: [
			{ text: '5千以下', value: 'A' },
			{ text: '5千-1万', value: 'B' },
			{ text: '1万以上', value: 'C' }
		]
	},
	{
		title: '营业执照',
		name: 'license',
		options: [
			{ text: '1年以内', value: 'A' },
			{ text: '1年以上', value: 'B' }
		]
	}
];

$('input', '#occupation').on('change', function(){
	var self = $(this);
	$('#form-salary-box').css('display', 'block');
	if (self.val() == 'A') {
		$('#form-salary-box').attr('class', 'form-salary-box office-work');
		STATIC.createHtml(office);
	} else if (self.val() == 'B') {
		$('#form-salary-box').attr('class', 'form-salary-box civil-servant');
		STATIC.createHtml(civil);
	} else if (self.val() == 'C') {
		$('#form-salary-box').attr('class', 'form-salary-box private-owner');
		STATIC.createHtml(private);
	}
});

// 选择复选框
$('#agree-btn').on('click', function(){
	if ($(this).is(':checked')) {
		$('input[name="agree"]').val('Y');
	} else {
		$('input[name="agree"]').val('N');
	};
});

// 表单提交
$('#submit-btn').on('click', function(e){
	var valid = true;

	if (valid) {
		$('.form-item-box', '#form-box').each(function(index, item){
			var flag = false;
			$('input', $(item)).each(function(_index, _item){
				if ($(_item).is(':checked')) {
					flag = true;
				}
			});
			if (!flag) {
				valid = false;
				salert('请还有选择题未作答');
				return false;
			}
		});
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
			type: 'post',
			url: $('#get-middle-interface').val(),
			data: UTIL._formatData($('#form-box')),
			success: function (response) {
				if (response.status == 0) {
					$.cookie('question', 'yes', { path: '/' });
					window.location.href = response.page_url;
				} else {
					salert(response.msg || '操作失败...');
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

// 保险条款
$('#to-see-detail').on('click', function(){
	if ($('#insurance-box').length > 0) {
		$('tr', '#insurance-box table').css('display', 'table-row');
		$(this).remove();
	}
});

// 弹窗
$('a', '#agree-box').on('click', function(){
	var self = $(this);
	if (self.text() == '账户资金安全险') {
		STATIC.modalHtml(self.text(), safetyInsurance);
	} else if (self.text() == '出行险') {
		STATIC.modalHtml(self.text(), travelInsurance);
	}
});

$('span', '#modal-box h3').on('click', function(){
	$('#mask, #modal-box').css('display', 'none');
});


