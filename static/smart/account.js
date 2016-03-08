function get_base(){
	$.ajax({
		type:"GET",
		url:"/account/list",
		success:function(data){
			if(!$.isEmptyObject(data)){
				var base = $("<div>用户名："+data.name+
						"<br/>邮箱:"+data.email+
						"<br/>积分："+data.point+"</div>");
				base.appendTo($("#na-e-p"));
				
				var img = $("<img src='"+data.head+"'class='img-polaroid'>");
				img.appendTo($(".thumbnail"));
			}
		}
	});
}

function get_opinion(){
	$.ajax({
		type:"GET",
		url:"/account/opinion",
		success:function(data){
			if(!$.isEmptyObject(data)){
				$.each(data,function(n,v){
					var topic = $("<tr class='toTopic' id='"+v.topicId+"'>" +
							"<td>"+v.topicName+"</td>" +
									"<td>"+v.time+"</td></tr>");
					topic.appendTo($("#o-all"));
				});
			}
		}
	});
}

function get_topic(){
	$.ajax({
		type:"GET",
		url:"/account/topic",
		success:function(data){
			if(!$.isEmptyObject(data)){
				$.each(data,function(n,v){
					var topic = $("<tr class='toTopic' id='"+v.topicId+"'>" +
							"<td>"+v.topicName+"</td>" +
									"<td>"+v.time+"</td></tr>");
					topic.appendTo($("#t-all"));
				});
			}
		}
	});
}

$(function toTopic(){
	$("body").on('click',"tr[class='toTopic']",function(){
		$.cookie("bbsid",$(this).attr("id"),{path:"/bbs/"});
		location.href = "/bbs/topic";
	});
})
function changePW(){
	$("#sub-val").click(function(){
			$("#PWch").toggle();
	})
}

$(function initial(){
	get_base();
	get_topic();
	get_opinion();
	$("#PWch").hide();
	changePW();
}) 




