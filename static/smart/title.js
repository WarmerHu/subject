authorId = "";
dataId = "";
time = 1;
answer = "";
function sudata(data){
	if(!$.isEmptyObject(data)){
			$('#title').html(data.title);
			$('#au').html("发布者："+data.author);
			$("#linkearticle").html(data.contribute);
			if(data.complaint){
				$("#cmp").html("取消投诉");
				$("#cmp").attr("cc","canC");
			}
//			if(data.state == 'ACTIVE'){
//				$('#state').html("此题未经审核，可选择跳过");
//				$('#skip').show();
//			}else{
//				$('#skip').hide();
//				$('#state').html("");
//			}
				answer = data.answer;
				authorId = data.authorid;
				$("#linkearticle").html(data.contribute);
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
		$('#CMs').hide();
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
  		});
  	
  	contri();
  	
  	$("#seeA").click(function(){
		$("input[name='answer']").val(answer).focus();
	});
  	
	$("#sub-val").click(function() {
		$.ajax({
			type: "POST",
			url: "/title/answer/check/",
			dataType: "json",
			timeout: 1000,
			data:JSON.stringify({
					'id':dataId,
					'answer':$.trim($("#sub-ans").val()),
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
		});
	});
})


function contri(){
		$("#contribute").click(function(){
			$.ajax({
	  			type:"POST",
	  			url:"/title/contribute/",
	  			dataType:"json",
	  			data:JSON.stringify({'titleid':dataId,"authorid":authorId}),
	  			success:function(data){
	  				linka = parseInt($("#linkearticle").html());
	  				linka += 1;
	  				$("#linkearticle").html(linka);
	  			},
	  			error:function(){
	  				alert("失败");
	  			}
	  		});
		});
}
$(function(){
	$("#complaint").click(function(){
		str = $("#cmp").attr("cc");;
		if(str=='addC'){
			$("#CMs").toggle();
			$("#submit").click(function(){
				addComplaint();
			});
		}else if(str=='canC'){
			cancelComplaint();
		}
	});
})
function cancelComplaint(){
		$.ajax({
	        type: "POST",
	        url: "/complaint/cancel/",
	        dataType: "json",
	        timeout: 1000,
	        data:JSON.stringify({'titleid':dataId}),
	        error: function(){
	        	alert("取消投诉失败");
	        },
	        success: function(data){
	        		$("#cmp").html("投诉");
	        		$("#cmp").attr("cc","addC");
	        		$("#tips").html(data.tips).show();
	        }
			});
}  	
function addComplaint(){
		content = 	$.trim($('textarea[name="reason"]').val());
		if(!content || content.length<10){
			$("#tips").html("请正确输入投诉理由").show();
		}else{
		jsonData = {
//					'titleid':dataId,
					'content':content
			}
			value = $('input:radio[name="radio"]:checked').val();
			if(value=='title'){
				jsonData['titleid'] = dataId; 
			}else if(value=='author'){
				jsonData['authorid'] = authorId;
			}
			$.ajax({
		        type: "POST",
		        url: "/complaint/add/",
		        dataType: "json",
		        timeout: 1000,
		        data:JSON.stringify(jsonData),
		        error: function(){
		        	alert("提交投诉失败");
		        },
		        success: function(data){
		        		$("#tips").html(data.tips).show();
		        		$("#cmp").html("取消投诉");
		        		$("#cmp").attr("cc","canC");
		        }
				});
		}
	}
//$(function sk(){
//		$('#skip').click(function(){
//				$.ajax({
//		  			type:"GET",
//		  			url:"/title/elist/"+(time+1),
//		  			dataType:"json",
//			        error: function(){
//			        	alert("获取下一题失败");
//			        },
//			        success: function(data){
//			        	sudata(data);
//			        	}
//				})
//		});
//	})