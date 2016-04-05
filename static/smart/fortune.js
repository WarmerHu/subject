$(function initial(){
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
					console.log("s");
			},
			error:function(){
				$("#tips").html("获取资源列表失败");
			}
			});
  	})   
