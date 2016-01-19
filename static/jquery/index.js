function get_activity(){
	$.ajax({
			type:"GET",
			url:"/activity/list/8",
			dataType:"json",
			success:function(data){
				$.each(data,function(n,value){
					    var parentdiv=$("<tr><td><pre>"+value+"</pre></td></tr>");   
					    parentdiv.appendTo($("#col-list"));
					});
				},
			error:function(){
				console.log("获取动态失败");
			}
			})
}

$(function initial(){
	get_activity();
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