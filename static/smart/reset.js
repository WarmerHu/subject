  	
$(function check(){
	$("#sub-val").click(function(){
		var reg =/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/;
		
		var usps = $.trim($("input[name='password']").val());
		var usre = $.trim($("input[name='re_password']").val());
		var use = $.trim($("input[name='email']").val());
		
		if(usps.length<6 || usps.length>20 || !usps || usps!=usre){
			$("#tips").html("请输入正确的密码").show();
		}
		else if(!use || !reg.test(use)){
			$("#tips").html("请输入正确的邮箱").show();
		}
		else{
			$.ajax({
				type:"POST",
				url:"/account/reset/",
				dataType:"json",
				data:JSON.stringify({
					'password':$.md5(usps),
					'email':use
				}),
				success:function(result){
					if("error" in result){
						$("#tips").html(result.error).show();
					}else if($.isEmptyObject(result)){
						$("div[class='panel panel-info']").remove();
						$("div[id='tips']").remove();
						var su = $("<div class='alert alert-success'>更改密码成功，请登录邮箱，并完成激活！</div>");
						su.appendTo($(".col-md-6"));
					}
				},
				error:function(result){
					alert("请求错误");
				}
			});
		}
	})
})