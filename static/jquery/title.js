  
dataId = "";
time = 1;

	$(function(){
  		if($.cookie("username")){
  			$("#islog").html("退出登录");
  			$("#reallog").html($.cookie("username"));
  			$("#islog").attr("href","/account/logout");
  		}else{
  			location.href = "/account/go_login";
  		}
  	})  

$(function()
  	{$('#tips').hide();}
  	)
  	
  	$(function initial(){
  		$.ajax({
  			type:"GET",
  			url:"/title/elist/1",
  			dataType:"json",
  			success:function(data){
  				if(data){
  					$('#title').html(data.title);
  					dataId = data.id;
  				}
  				else{
  					location.href = "/account/go_login";
  				}
  			},
  			error:function(){
  				alert("失败");
  			}
  		})
  	})

  	$(function check() {
  		$("#sub-val").click(function() {
  				$.ajax({
			        type: "POST",
			        url: "/title/answer/check/",
			        dataType: "json",
			        timeout: 1000,
			        data:JSON.stringify({
					'id':dataId,
					'answer':$("#sub-ans").val(),
					'num':time+1
				}),
			        error: function(){
			        	alert("获取下一题失败");
			        },
			        success: function(data){
			        if(data.tips){
			            $("#tips").html(data.tips).show();
			        }
			        else{
			        	$("#title").html(data.title);
			        	$("input[name='answer']").val("").focus();
		  				dataId = data.id;
		  				time += 1;
		  				}
			        }
		})
	}
  			  )
  	})