bbsid = $.cookie("bbsid");
curNum = 0;
curAU = 0;
curOP = 0;
ph = 0;

function getHeight(that){
	authorh = $(that).children(".p_author").outerHeight(true)+30;
	contenth = $(that).children(".p_content").outerHeight(true);
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
					var parentdiv = $("<div class='p_postlist' id='op-"+v.id+"'></div>");
					var authordiv = $("<ul class='p_author'></ul>");
					var imgInAuthordiv = $("<li>" +
							"<a class='p_author_face' target='_blank'>" +
							"<img src='"+v.head+"'></a></li>");
					var nameInAuthordiv = $("<li>" +
							"<a class='p_author_name j_user_card' target='_blank' alog-group='p_author'>"+v.name+"</a></li>");
					var timeInAuthordiv = $("<br><li>"+v.time+"</li><li class='opNUM'>#"+(n+curNum)+"</li>");
					if(v.complaint){
						var combut = "<li><button type='button' class='btn btn-default complaintO' id='' au='"+v.authorid+"' op='"+v.id+"' tp=''>"+
						"<i class='glyphicon glyphicon-thumbs-down'></i>"+
						"<span class='cmp'  cc='can'>取消投诉</span></button>"
					}else{
						var combut = "<li><button type='button' class='btn btn-default complaintO' id='' au='"+v.authorid+"' op='"+v.id+"' tp=''>"+
						"<i class='glyphicon glyphicon-thumbs-down'></i>"+
						"<span class='cmp'  cc='add'>投诉</span></button>"
					}
					var buttondiv = $( combut+	"<button type='button' class='btn btn-default quoteO' id='' au='"+v.authorid+"' op='"+v.id+"' tp=''>"+
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
				getHeight(this);
				if(data.complaint){
					$(".cmp").html("取消投诉");
					$(".cmp").attr("cc","can");
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
        	if(data.tips){
        		alert(data.tips);
        	}else{
        		$(that).children(".cmp").html("投诉");
        		$(that).children(".cmp").attr("cc","add");
        		}
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
		var value = $('input:radio[name="radio"]:checked').val();
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
	        	}else if(value=='topic' ||  value=='opinion'){
	        		$(that).children(".cmp").html("取消投诉");
	        		$(that).children(".cmp").attr("cc","can");
	        		$("#CMs").hide();
	        	}
	        }
			});
	}
}
function com(that){
	$(".submitT").attr("au",$("#complaintT").attr("au"));
	str = $(that).children(".cmp").attr("cc");
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
		$("#opinion").removeAttr("checked");
		$("#topic").removeAttr("disabled");
		$("#opinion").attr("disabled","true");
		$("#topic").prop("checked","checked");
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
		$("#opinion").prop("checked","checked");
		$("#topic").attr("disabled","true");
		$(".submitT").attr("op",$(this).attr("op"));
		com(this);
	});
	$("body").on('click',".quoteO",function(){
		var opid = parseInt($(this).attr("op")); 
		var par = $(this).parent().parent();
		ph = par.children(".opNUM").html();
		curAU = parseInt($(this).attr("au"));
		curOP = "#op-"+opid;
		$("#detail").val("<b>引用<a href='"+curOP+"'>"+ph+"</a>的意见</b>\n");
		$("#detail").focus();
		$(this).scrollTo('#pu-opi');
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
					"au":curAU,
					"op":curOP,
					"ph":ph
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
