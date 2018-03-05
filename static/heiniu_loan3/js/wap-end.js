// 刷新页面滚动顶部
$('html, body').scrollTop(0);
$('#mask').height($(document).height() > $(window).height()
				  ? $(document).height()
				  : $(window).height());

// tab切换
$('a', '.suggest-nav-box').on('click', function () {
	var self = $(this);
	$('a', '.suggest-nav-box').removeClass('active');
	self.addClass('active');
	$('.suggest-content-box').css('display', 'none');
	$('.suggest-content-box').eq(self.index()).css('display', 'block');
});

// 弹窗显示
var timer = null;
var num = 5;
$('#free-get-btn').on('click', function (){
	$.ajax({
		type: 'get',
		url: '/activity/hnyouqianclick3',
		success: function(response){
			if (response.data.policy_no !== '') {
				clearInterval(timer);
				var data = response.data;
				var str = '';
				$('h4', '#modal-insurance-box').html('<img src="'+ $('#static-host').val() +
				'/static/images/logos/wap_'+ data.policy_company +
				'.png" alt="">' + data.policy_name);
				$.each(data.policy_infos, function(index, item){
                    str += '<tr><td>'+ item.content +'</td><td>'+ item.amount +'</td></tr>';
                });
                $('tbody', '#modal-insurance-box .table-box').html('').html(str);

				$('#modal-apply-box').css('display', 'none');
				$('#modal-insurance-box').css('display', 'block');
				timer = setInterval(function(){
					num--;
					$('span', '#close-insurance-box').text(num);
					if (num <= 0) {
						$('#mask, #modal-insurance-box').css('display', 'none');
						clearInterval(timer);
					}
				}, 1000);
			} else {
				$('#mask, #modal-apply-box').css('display', 'none');
				salert(response.error_msg || '操作失败...');
			}
		},
		error: function(){
			salert('网络繁忙，请稍后重试...');
		}
	});
});

$('#close-apply-box').on('click', function(){
	$('#mask, #modal-apply-box').css('display', 'none');
});
$('#close-insurance-box').on('click', function(){
	$('#mask, #modal-insurance-box').css('display', 'none');
});
