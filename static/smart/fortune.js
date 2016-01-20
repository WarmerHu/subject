$(function initial(){
  		if($.cookie("username")){
  			$("#islog").html("退出登录");
  			$("#reallog").html($.cookie("username"));
  			$("#islog").attr("href","/account/logout");
  			
  		}else{
  			$("#islog").html("登录");
  			$("#islog").attr("href","/account/go_login");
  		}
  		$.ajax({
				type:"GET",
				url:"/fortune/list",
				dataType:"json",
				success:function(data){
					if(!$.isEmptyObject(data)){
						$.each(data,function(n,value){
	  						var parentdiv=$("<tr><td>"+value.username+"</td><td>"+value.fortune+"</td></tr>");  
	  					    parentdiv.appendTo($("#col-list"));
						});
					}
					else{
						var content = $("<tr><td>暂无用户</td><td></td></tr>");
						content.appendTo($("#col-list"));
					}
			},
			error:function(){
				$("#tips").html("获取资源列表失败");
			}
			});
  	})   
