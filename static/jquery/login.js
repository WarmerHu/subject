$(function initial()
  	{$('#tips').hide();}
  	)
  	
$(function check(){
	$("#sub-val").click(function(){
		var usps = $.trim($("input[name='password']").val());
		var usna = $.trim($("input[name='username']").val());
		if(!usps || !usna){
			$("#tips").html("请输入正确的账号密码").show();
		}
		else{
			$.ajax({
				type:"POST",
				url:"/account/login/",
				dataType:"json",
				timeout:1000,
				data:JSON.stringify({
					'username':usna,
					'password':$.md5(usps)
				}),
				success:function(result){
					if("username" in result){
						$.cookie("username",result.username,{expires:7,path:"/"});
						location.href = "/";
					}else{
						$("#tips").html(result.error).show();						
					}
				},
				error:function(result){
					alert("请求错误");
				}
			});
		}
	})
})