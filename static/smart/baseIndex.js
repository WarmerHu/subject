
function out(){
	$("#islog").click(function(){
			$.removeCookie('username',{expires:7,path:"/"});
			$.removeCookie("userid",{expires:7,path:"/"});
			window.location.reload();//刷新当前页面
		});
}

$(function(){
  		if($.cookie("username")){
  			$("#islog").html("退出登录");
  			$("#reallog").html($.cookie("username"));
//  			$("#islog").attr("href","/account/logout");
  			out();
  			$('#tips').hide();
  		}else{
  			$("#islog").html("登录");
  			$("#islog").attr("href","/account/go_login");
  		}
  	})  


