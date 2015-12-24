$(function()
  	{$('#tips').hide();}
  	)
  	
$(function(){
	$("#sub-val").click(function(){
		var usps = $("input[name='password']").val();
		var usna = $("input[name='username']").val();
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
					'password':usps
				}),
				success:function(result){
					if($.cookie("name")){
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