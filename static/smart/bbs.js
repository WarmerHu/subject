function showData(p){
		$.ajax({
			type:"GET",
			url:"/bbs/list/?p="+p,
			dataType:"json",
			success:function(data){
				if(!$.isEmptyObject(data)){
					$("#col-list").children().remove();
					$.each(data.topic,function(n,v){
  						var parentdiv=$("<tr class='toTopic' id='"+v.id+"'><td>"+v.title+"</td>" +
  								"<td>"+v.publisher+"</td>" +
  								"<td class='td-t'>"+v.replyTime+"</td>" +
  								"<td>"+v.createTime+"</td>" +
  								"<td>"+v.modifyTime+"</td></tr>");  
  					    parentdiv.appendTo($("#col-list"));
					});
					if(data.numT){
						pageCount = Math.ceil(data.numT / 20);
						paging(pageCount,".pagination");
					}
				}
				else{
					var content = $("<tr><td>暂无话题</td><td></td><td></td><td></td><td></td></tr>");
					content.appendTo($("#col-list"));
				}
		},
		error:function(){
			var content = $("<tr><td>获取话题列表失败</td><td></td><td></td><td></td><td></td></tr>");
			content.appendTo($("#col-list"));
		}
		});
}
$(function initial(){
	showData(0);
})   

$(function toTopic(){
	$("body").on('click',"tr[class='toTopic']",function(){
		$.cookie("bbsid",$(this).attr("id"));
		location.href = "/bbs/topic";
	});
})
  	
/*
 * 发布话题：
 * 1.验证登录信息&数据格式：正确，下一步；否，tips
 * 2.ajax提交数据，并获取返回信息：有tips，显示tips；否，将id写入cookie，跳转页面至新发布的话题
 * */
  	$(function publish(){
	$("#add-val").click(function(){
		if(!$.cookie("username")){
			$("#tips").html("请先登录").show();
		}else{
		var name = $.trim($("input[name='name']").val());
		var detail = $.trim($("textarea[name='detail']").val());
		
		if(name.length<6 || name.length>50 || detail.length<10){
			$("#error").html("请正确描写标题与详情").show();
		}
		else{
			$.ajax({
				type:"POST",
				url:"/bbs/publish/",
				dataType:"json",
				timeout:1000,
				data:{
					'name':name,
					'detail':detail
				},
				success:function(result){
					if("tips" in result){
						$("#error").html(result.tips).show();
					}else{
						$.cookie("bbsid",result.id);
						location.href = "/bbs/topic";
					}
				},
				error:function(result){
					$("#error").html("请求错误").show();
				}
			});
		}
		}
	});
})
