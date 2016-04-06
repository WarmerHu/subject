function showData(p){
	$("#col-list").children().remove();
	$.ajax({
		type:"GET",
		url:"/fortune/list/?p="+p,
		dataType:"json",
		success:function(data){
			if(!$.isEmptyObject(data)){
				if(data.numT){
					pageCount = Math.ceil(data.numT / 20);
					paging(pageCount，".pagination");
				}
				$.each(data.fortune,function(n,value){
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
}

$(function initial(){
  	showData(0);
  	})   
