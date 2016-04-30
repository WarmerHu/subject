  	
$(function check(){
	$("#sub-val").click(function(){
		var reg =/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/;
		
		var usps = $.trim($("input[name='password']").val());
		var usre = $.trim($("input[name='re_password']").val());
		var usna = $.trim($("input[name='username']").val());
		var use = $.trim($("input[name='email']").val());
		
		if(usna.length<2 || usps.length<6 || usps.length>20 || !usps || !usna){
			$("#tips").html("请输入正确的账号密码").show();
		}
		else if(!use || !reg.test(use)){
			$("#tips").html("请输入正确的邮箱").show();
		}
		else if(usps!=usre){
			$("#tips").html("密码不一致").show();
		}
		else{
			$.ajax({
				type:"POST",
				url:"/account/regist/",
				dataType:"json",
				data:JSON.stringify({
					'username':usna,
					'password':$.md5(usps),
					'email':use
				}),
				success:function(result){
					if("error" in result){
//						$.cookie("username",result.username,{expires:7,path:"/"});
//						location.href = "/";
						$("#tips").html(result.error).show();
					}else if($.isEmptyObject(result)){
						$("div[class='panel panel-info']").remove();
						$("div[id='tips']").remove();
						var su = $("<div class='alert alert-success'>注册成功，请登录邮箱，并完成激活！</div>");
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