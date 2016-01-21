$(function () {
	var ie6 = document.all;
	var dv = $('#fixedMenu_keleyi_com'), st;
	dv.attr('otop', dv.offset().top); //存储原来的距离顶部的距离
	$(window).scroll(function () {
		st = Math.max(document.body.scrollTop || document.documentElement.scrollTop);
		if (st > parseInt(dv.attr('otop'))) {
			if (ie6) {//IE6不支持fixed属性，所以只能靠设置position为absolute和top实现此效果
				dv.css({ position: 'absolute', top: st });
			}
			else if (dv.css('position') != 'fixed') dv.css({ 'position': 'fixed', top: 0 });
		} else if (dv.css('position') != 'static') dv.css({ 'position': 'static' });
	});
});