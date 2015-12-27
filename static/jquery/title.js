  
dataAsw = "";
dataId = "";
dataTips = "";

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
  	
  	$(function(){
  		$.ajax({
  			type:"GET",
  			url:"/elist/1",
  			dataType:"json",
  			success:function(data){
  				$('#title').html(data.title);
  				dataAsw = data.answer;
  				dataId = data.id;
  				dataTips = data.tips;
  			},
  			error:function(){
  				alert("失败");
  			}
  		})
  	})
  	
    $(function() {
  		$("#sub-val").click(function() {
  			if(dataAsw != $("#sub-ans").val()){
  				if(dataTips){
  					$("#tips").html(dataTips).show();
  				}
  				else{
  					$("#tips").html("无提示").show();
  				}
				
			}
  			else{
  				nextId =  dataId+1;
  				$.ajax({
			        type: "GET",
			        url: "/elist/"+nextId,
			        dataType: "json",
			        timeout: 1000,
			        error: function(){
			        	alert("获取下一题失败");
			        },
			        success: function(data){
			        	$("#title").html(data.title);
			        	$("input[name='answer']").val("").focus();
		  				dataAsw = data.answer;
		  				dataId = data.id;
		  				dataTips = data.tips;
			        }
			      })
			 }
		})
	}
  			  )