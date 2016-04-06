bbsid = $.cookie("bbsid");
curNum = 0

function getHeight(){
	authorh = $(".p_author").outerHeight(true)+30;
	contenth = $(".p_content").outerHeight(true);
	if(authorh>contenth){
		$(".p_postlist").css("height",authorh);
	}else{
		$(".p_postlist").css("height",contenth);
	}
}
function showData(p){
	getOpinion(bbsid,p);
}
function getOpinion(bbsid,p){
	cur = p==0?1:p;
	curNum = (cur-1)*20+1
	$("#opi-all").children().remove();
	$.ajax({
		type:"GET",
		url:"/bbs/topic/O/list/"+bbsid+"/?p="+p,
		dataType:"json",
		success:function(data){
			if(!$.isEmptyObject(data)){
				if(data.numT){
					pageCount = Math.ceil(data.numT / 20);
					paging(pageCount,".pagination");
				}
				$.each(data.opinion,function(n,v){
					var parentdiv = $("<div class='p_postlist'></div>");
					var authordiv = $("<ul class='p_author'></ul>");
					var imgInAuthordiv = $("<li>" +
							"<a class='p_author_face' target='_blank'>" +
							"<img src='"+v.head+"'></a></li>");
					var nameInAuthordiv = $("<li>" +
							"<a class='p_author_name j_user_card' target='_blank' alog-group='p_author'>"+v.name+"</a></li>");
					var timeInAuthordiv = $("<br><li>"+v.time+"</li><li>#"+(n+curNum)+"</li>");
					imgInAuthordiv.appendTo(authordiv);
					nameInAuthordiv.appendTo(authordiv);
					timeInAuthordiv.appendTo(authordiv);
					
					var contentdiv = $("<div class='p_content'>" +
							"<pre>"+v.content+"</pre></div>");
					authordiv.appendTo(parentdiv);
					contentdiv.appendTo(parentdiv);
					
					parentdiv.appendTo($("#opi-all"));
					getHeight();
				});
				
			}
	},
	error:function(){
		$("#opi").html("获取意见详情失败");
	}
	});
}

function getTopic(bbsid){
	$.ajax({
		type:"GET",
		url:"/bbs/topic/list/"+bbsid,
		dataType:"json",
		success:function(data){
			if(!$.isEmptyObject(data)){
				$("h1[name='title-topic']").html(data.topic);
				$("input[name='title-id']").html(data.id);
				$("cc").html(data.replayTime);
				$("#title-imgs").attr("src",data.head);
				$("#title-author").html(data.author);
				$("#title-time").html(data.creatTime);
				$("#title-content").html(data.content);
				getHeight();
			}
			else{
				$("#opi").html("没有该则话题");
			}
	},
	error:function(){
		$("#opi").html("获取话题详情失败");
	}
	});
}
$(function initial(){
	$('#tips').hide();
	getTopic(bbsid);
	getOpinion(bbsid,0);
})   

$(function publish(){
	$("#add-val").click(function(){
		var detail = $.trim($("#detail").val());
		if(detail.length>=10){
			bbsid = $.cookie("bbsid");
			$.ajax({
				type:"POST",
				url:"/bbs/topic/"+bbsid+"/publish",
				dataType:"json",
				data:{
					"content":detail,
				},
				success:function(result){
					if($.isEmptyObject(result)){
						window.location.reload();//刷新当前页面
					}else{
						$("#tips").html(result.tips).show();
					}
				},
				error:function(){
					
				}
			});
		}else{
			$("#tips").html("请正确输入意见").show();
		}
	});
})
