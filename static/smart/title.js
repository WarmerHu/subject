  
dataId = "";
time = 1;
function sudata(data){
	if(!$.isEmptyObject(data)){
			$('#title').html(data.title);
			$('#au').html("发布者："+data.author);
			if(data.state == 'ACTIVE'){
				$('#state').html("此题未经审核，可选择跳过");
				$('#skip').show();
			}else{
				$('#skip').hide();
				$('#state').html("");
			}
    	$("input[name='answer']").val("").focus();
			dataId = data.id;
			time += 1;
			$("#tips").hide();
    }else{
    	$("#tips").html("正解").show();
    	alert("这是最后一题");
    }
}
	$(function initial(){
		$('#skip').hide();
  		$.ajax({
  			type:"GET",
  			url:"/title/elist/1",
  			dataType:"json",
  			success:function(data){
  				sudata(data);
  				time -= 1;
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
			        	}else{
			        		sudata(data);
			        	}
			        }
  				})
  		})
  	})
  
$(function sk(){
		$('#skip').click(function(){
				$.ajax({
		  			type:"GET",
		  			url:"/title/elist/"+(time+1),
		  			dataType:"json",
			        error: function(){
			        	alert("获取下一题失败");
			        },
			        success: function(data){
			        	sudata(data);
			        	}
				})
		});
	})