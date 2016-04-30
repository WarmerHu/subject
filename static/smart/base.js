	$(function(){
  		if($.cookie("username")){
  			$("#islog").html("退出登录");
  			$("#reallog").html($.cookie("username"));
  			$("#islog").attr("href","/account/logout");
  			$('#tips').hide();
  		}else{
  			location.href = "/account/go_login";
  		}
  	})  

