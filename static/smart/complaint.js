which = '';
function showData(p){
	if(which=="for"){
		forMEajax(p);
	}else if(which=="from"){
		fromMEajax(p);
	}
}
function cancelCom(that){
	tp = parseInt($(that).attr("tp"));
	op = parseInt($(that).attr("op"));
	tl = parseInt($(that).attr("tl"));
	rs = parseInt($(that).attr("rs"));
	au = parseInt($(that).attr("au"));
	jsonData = {};
	if(tp){
		jsonData['topicid'] = tp;
	}else if(op){
		jsonData['opinionid'] = op;
	}else if(tl){
		jsonData['titleid'] = tl;
	}else if(rs){
		jsonData['rsid'] = rs;
	}else if(au){
		jsonData['authorid'] = au;
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
        		$(that).parent().parent().remove();
        		}
        }
		});
}  
function fromMEajax(p){
	$("#com").children().remove();
	$.ajax({
		type:"GET",
		url:"/complaint/individual/me/from/?p="+p,
		dataType:"json",
		success:function(data){
			if(!$.isEmptyObject(data)){
				if(data.numT){
					pageCount = Math.ceil(data.numT / 20);
					paging(pageCount,".pagination");
				}
				$.each(data.result,function(n,value){
					var parentdiv = $("<div class='com-all'></div>")
					var fromdiv = $("<div> 我的投诉：</div>");
					var contentdiv = $("<div><pre>"+value.content+"</pre></div>")
					var butdiv = '';
					fromdiv.appendTo(parentdiv);
					contentdiv.appendTo(parentdiv);
					var condiv = $("<div class='af-con'></div>");
					if(value.titleid){
						var titlediv = $("<div> <a href='' ex='"+value.titleid+"' au='"+value.titleauid+"'>"+value.titleauname+"&nbsp发布的题目：<br /><pre>"+value.titlename+"</pre></a></div>");
						butdiv = $("<div class='canbtn'><button class=‘btn btn-default ’ tl='"+value.titleid+"' rs='' tp='' op='' au='' ><span  class='glyphicon glyphicon-remove' aria-hidden='true'></span>取消投诉</button></div>");
						titlediv.appendTo(condiv);
					}else if(value.rsid){
						var rsdiv = $("<div> <a href='' rs='"+value.rsid+"' au='"+value.rsauid+"'>"+value.rsauname+"&nbsp发布的资源："+value.rsname+"</a></div>");
						butdiv = $("<div class='canbtn'><button class=‘btn btn-default’ rs='"+value.rsid+"'  tl='' tp='' op='' au='' ><span  class='glyphicon glyphicon-remove' aria-hidden='true'></span>取消投诉</button></div>");
						rsdiv.appendTo(condiv);
					}else if(value.tpid){
						$.cookie("bbsid",value.tpid);
						var tpdiv = $("<div> <a href='/bbs/topic' au='"+value.tpauid+"'>"+value.tpauname+"&nbsp发布的话题：<br /><pre>"+value.tpname+"</pre></a></div>");
						butdiv = $("<div class='canbtn'><button class=‘btn btn-default’ tp='"+value.tpid+"'  rs='' tl='' op='' au='' ><span  class='glyphicon glyphicon-remove' aria-hidden='true'></span>取消投诉</button></div>");
						tpdiv.appendTo(condiv);
					}else if(value.opid){
						$.cookie("bbsid",value.optpid);
						var opdiv = $("<div> <a href='/bbs/topic' au='"+value.opauid+"'>"+value.opauname+"&nbsp发表的意见：<br /><pre>"+value.opname+"</pre><br />来自话题："+value.optpname+"</a></div>");
						butdiv = $("<div class='canbtn'><button class=‘btn btn-default ’ op='"+value.opid+"'  rs='' tp='' tl='' au=''><span  class='glyphicon glyphicon-remove' aria-hidden='true'></span>取消投诉</button></div>");
						opdiv.appendTo(condiv);
					}else if(value.auid){
						var audiv = $("<div> <a href='' au='"+value.auid+"'>用户："+value.auname+"</a></div>");
						butdiv = $("<div class='canbtn'><button class=‘btn btn-default ’ au='"+value.auid+"'  rs='' tp='' op='' tl='' ><span  class='glyphicon glyphicon-remove' aria-hidden='true'></span>取消投诉</button></div>");
						audiv.appendTo(condiv);
					}
					butdiv.appendTo(parentdiv);
					condiv.appendTo(parentdiv);
					parentdiv.appendTo($("#com"));
			});
			}else{
					$("#com").html("你没有收到任何投诉。");
			}
	},
	error:function(){
		$("#tips").html("获取失败");
	}
	});
}
function forMEajax(p){
	$("#com").children().remove();
	$.ajax({
		type:"GET",
		url:"/complaint/individual/me/?p="+p,
		dataType:"json",
		success:function(data){
			if(!$.isEmptyObject(data)){
				if(data.numT){
					pageCount = Math.ceil(data.numT / 20);
					paging(pageCount,".pagination");
				}
				$.each(data.result,function(n,value){
					var parentdiv = $("<div class='com-all'></div>")
					var fromdiv = $("<div><button class='btn btn-link' fm='"+value.fromid+"'>来自 "+value.fromname+"("+value.fromemail+")的投诉：</button> </div>");
					var contentdiv = $("<div><pre>"+value.content+"</pre></div>")
					fromdiv.appendTo(parentdiv);
					contentdiv.appendTo(parentdiv);
					var condiv = $("<div class='af-con'></div>");
					if(value.titleid){
						var titlediv = $("<div> <a href='' ex='"+value.titleid+"'>原题：<br /><pre>"+value.titlename+"</pre></a></div>");
						titlediv.appendTo(condiv);
					}else if(value.rsid){
						var rsdiv = $("<div> <a href='' rs='"+value.rsid+"'>原资源："+value.rsname+"</a></div>");
						rsdiv.appendTo(condiv);
					}else if(value.tpid){
						$.cookie("bbsid",value.tpid);
						var tpdiv = $("<div> <a href='/bbs/topic'>原话题：<br /><pre>"+value.tpname+"</pre></a></div>");
						tpdiv.appendTo(condiv);
					}else if(value.opid){
						$.cookie("bbsid",value.optpid);
						var opdiv = $("<div> <a href='/bbs/topic'>原意见：<br /><pre>"+value.opname+"</pre><br />来自话题："+value.optpname+"</a></div>");
						opdiv.appendTo(condiv);
					}else if(value.auid){
						var audiv = $("<div> <a href='' au='"+value.auid+"'>你本人（"+value.auname+"）被投诉</a></div>");
						audiv.appendTo(condiv);
					}
					condiv.appendTo(parentdiv);
					parentdiv.appendTo($("#com"));
			});
			}else{
					$("#com").html("你没有收到任何投诉。");
			}
	},
	error:function(){
		$("#tips").html("获取失败");
	}
	});
}

function forME(p){
	which="for";
	$(".pagination>li").children(".nt").remove();
	showData(p);
}
function fromME(p){
	which="from";
	$(".pagination>li").children(".nt").remove();
	showData(p);
}
$(function initial(){
	forME(0);
	 $("body").on('click',".canbtn",function(){
		 	var that = $(this).children("button");
		 	cancelCom(that);
	 });
})