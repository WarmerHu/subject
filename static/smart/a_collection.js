 time = 1;
 function addData(data){
		$("strong[name='right']").html(data.rightTime);
			$("strong[name='wrong']").html(data.wrongTime);
			$("input[name='col-id']").val(data.id);
			$("input[name='col-title-id']").val(data.title.id);
			$('#title').html(data.title.title);
 }
  	function initial(){
  		$.ajax({
  			type:"GET",
  			url:"/collection/Clist/1",
  			dataType:"json",
  			success:function(data){
  				if(!$.isEmptyObject(data)){
  					addData(data);
  				}
  				else{
  					$("#tips").html("获取失败，请重新登录or重新获取");
  				}
  			},
  			error:function(){
  				alert("获取错题失败");
  			}
  		})
  	}	
  	$(function(){
  		if($.cookie("username")){
  			$("#islog").html("退出登录");
  			$("#reallog").html($.cookie("username"));
  			$("#islog").attr("href","/account/logout");
  			$('#tips').hide();
  			initial();
  		}else{
  			location.href = "/account/go_login";
  		}
  	})  	


  	$(function check() {
  		$("#sub-val").click(function() {
  				$.ajax({
			        type: "POST",
			        url: "/collection/answer/check/",
			        dataType: "json",
			        timeout: 1000,
			        data:JSON.stringify({
			        	"id":$("input[name='col-id']").val(),
			        	"title":{
			        		"id":$("input[name='col-title-id']").val(),
			        		"answer":$("#sub-ans").val().trim()
			        	},
			        	"num":time+1
				}),
			        error: function(){
			        	alert("提交失败");
			        },
			    success: function(data){
			    	if($.isEmptyObject(data)){
			    		$("#tips").html("这是最后一题,已无下一题").show();
			    	}else{
				        if(data.tips){
				            $("#tips").html(data.tips).show();
				            if(data.wrongTime){
				            	$("strong[name='wrong']").html(data.wrongTime);			            	
				            }
				        }
				        else{
				        	addData(data);
			  				time += 1;
			  				}
			    	}

			    }
		})
	}
  			  )
  	})