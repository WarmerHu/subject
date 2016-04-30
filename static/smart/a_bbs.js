bbsid = $.cookie("bbsid");
curNum = 0

function getHeight(that){
	authorh = $(that).children(".p_author").outerHeight(true)+30;
	contenth = $(that).children(".p_content").outerHeight(true);
	console.log(authorh);
	console.log(contenth);
	console.log(that);
	console.log($(that).children(".p_author"));
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
					var buttondiv = $("<li><button type='button' class='btn btn-default complaintO' id='' au='"+v.authorid+"' op='"+v.id+"' tp=''>"+
							"<i class='glyphicon glyphicon-thumbs-down'></i>"+
					"<span class='cmp'  cc='add'>投诉</span></button>" +
					"<button type='button' class='btn btn-default quoteO' id='' au='"+v.authorid+"' op='"+v.id+"' tp=''>"+
							"<i class='glyphicon glyphicon-thumbs-up'></i>"+
					"<span class='quo'  cc='addO'>引用</span></button></li>");
					imgInAuthordiv.appendTo(authordiv);
					nameInAuthordiv.appendTo(authordiv);
					timeInAuthordiv.appendTo(authordiv);
					buttondiv.appendTo(authordiv);
					
					var contentdiv = $("<div class='p_content'>" +
							"<pre>"+v.content+"</pre></div>");
					authordiv.appendTo(parentdiv);
					contentdiv.appendTo(parentdiv);
//					getHeight(parentdiv);
					parentdiv.appendTo($("#opi-all"));
					
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
				$("#complaintT").attr("tp",data.id);
				$("#complaintT").attr("au",data.authorid);
				if(data.complaint){
					$("#cmpT").html("取消投诉");
					$("#cmpT").attr("cc","canT");
				}
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
function cancelComplaintT(that){
	tp = parseInt($(that).attr("tp"));
	op = parseInt($(that).attr("op"));
	jsonData = {};
	if(tp){
		jsonData['topicid'] = tp;
	}else if(op){
		jsonData['opinionid'] = op;
	}
	$.ajax({
        type: "POST",
        url: "/complaint/cancel/",
        dataType: "json",
        timeout: 1000,
        data:JSON.stringify(jsonData),
        error: function(){
        	alert("取消投诉失败");
        },
        success: function(data){
        		$("#cmpT").html("投诉");
        		$("#cmpT").attr("cc","addT");
        		$("#tips").html(data.tips).show();
        }
		});
}  	
function addComplaintT(that){
	content = 	$.trim($('textarea[name="reason"]').val());
	if(!content || content.length<10){
		alert("请正确输入投诉理由");
	}else{
	jsonData = {
				'content':content
		}
		value = $('input:radio[name="radio"]:checked').val();
		if(value=='topic'){
			jsonData['topicid'] = parseInt($(that).attr("tp"));
		}else if(value=='author'){
			jsonData['authorid'] = parseInt($(that).attr("au"));
		}else if(value=='opinion'){
			jsonData['opinionid'] = parseInt($(that).attr("op"));
		}
		$.ajax({
	        type: "POST",
	        url: "/complaint/add/",
	        dataType: "json",
	        timeout: 1000,
	        data:JSON.stringify(jsonData),
	        error: function(){
	        	alert("提交投诉失败");
	        },
	        success: function(data){
	        	if(data.tips){
	        		alert(data.tips);
	        	}else{
	        		$("#cmpT").html("取消投诉");
	        		$("#cmpT").attr("cc","canT");
	        	}
	        }
			});
	}
}
function com(that){
	$(".submitT").attr("au",$("#complaintT").attr("au"));
	str = $(that).children(".cmpT").attr("cc");;
	if(str=='add'){
		$("#RULE").hide();
		$("#CMs").toggle();
		$(".submitT").click(function(){
			addComplaintT(that);
		});
	}else if(str=='can'){
		cancelComplaintT(that);
	}
}
$(function initial(){
	$("#CMs").hide();
	$("#RULE").hide();
	$('#tips').hide();
	getTopic(bbsid);
	getOpinion(bbsid,0);
	$("#complaintT").click(function(){
		$("#opinion").attr("disabled","true");
		$("#topic").attr("checked","checked");
		$(".submitT").attr("tp",$("#complaintT").attr("tp"));
		com(this);
	});
	$("#regular").click(function(){
		$("#CMs").hide();
		$("#RULE").toggle();
	});
	$("body").on('click',".complaintO",function(){
		$("#opinion").removeAttr("disabled");
		$("#topic").removeAttr("checked");
		$("#opinion").attr("checked","checked");
		$("#topic").attr("disabled","true");
		$(".submitT").attr("op",$(this).attr("op"));
		com(this);
	});
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
