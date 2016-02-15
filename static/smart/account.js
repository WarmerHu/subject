function get_base(){
	$.ajax({
		type:"GET",
		url:"/account/list",
		success:function(data){
			if(!$.isEmptyObject(data)){
				var img = $("<img src='"+data.head+"'>");
				img.appendTo($(".thumbnail"));
				
				var base = $("用户名："+data.name+
						"<br/>邮箱:"+data.email+
						"<br/>积分："+data.point);
				base.appendTo($("#na-e-p"));
			}
		}
	});
}

function get_base(){
	$.ajax({
		type:"GET",
		url:"/account/topic",
		success:function(data){
			if(!$.isEmptyObject(data)){
				var img = $("<img src='"+data.head+"'>");
				img.appendTo($(".thumbnail"));
				
				var base = $("用户名："+data.name+
						"<br/>邮箱:"+data.email+
						"<br/>积分："+data.point);
				base.appendTo($("#na-e-p"));
			}
		}
	});
} 

$(function initial(){

})   

