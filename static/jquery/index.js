  	$(function(){
  		if($.cookie("username")){
  			$("#islog").html("退出登录");
  			$("#reallog").html($.cookie("username"));
  			$("#islog").attr("href","/account/logout");
  		}else{
  			$("#islog").html("登录");
  			$("#islog").attr("href","/account/go_login");
  		}
  	})  
  	

  	
  	$(function(){
  	$("#toTitle").click(function(){
  			if($.cookie("username")){
  				location.href = "/title";
  			}else{
  				alert("请先登录");
  				location.href = "/account/go_login";
  			}
  	})
  	})
  	
  	$(function toCollection(){
  	$("#toCollection").click(function(){
  			if($.cookie("username")){
  				location.href = "/collection";
  			}else{
  				alert("请先登录");
  				location.href = "/account/go_login";
  			}
  	})
  	})