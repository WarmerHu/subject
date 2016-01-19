
	$(function initial(){
		console.log("initial");
		$("#do-collection").hide();
		$("#tips").hide();
  		if($.cookie("username")){
  			console.log("退出登录");
  			$("#islog").html("退出登录");
  			$("#reallog").html($.cookie("username"));
  			$("#islog").attr("href","/account/logout");
  			$.ajax({
  				type:"GET",
  				url:"/collection/list",
  				dataType:"json",
  				success:function(data){
  					if(!$.isEmptyObject(data)){
  						console.log("data:",data);
  						$.each(data,function(n,value){
  	  						var parentdiv=$("<tr name='tr-" + n + "'></tr>");  
  	  					    var childdiv=$('<td></td>');   
  	  					    var content = $(
  	  					    		"<input type='hidden' name='col-id-"+ n +"' value=" + value.id + ">" + 
  	  					    		"<input type='hidden' name='col-title-id-"+n+ "' value=" + value.title.id + ">" +
  	  					    		"<button class='btn btn-info' name='del' id='" + n + "'>删除</button>" +
  	  					    		"&nbsp&nbsp&nbsp&nbsp正确次数：" + value.rightTime + "&nbsp&nbsp&nbsp&nbsp&nbsp错误次数：" + value.wrongTime +
  	  					    		"<br><b>题目:</b>" +"<pre>" +	value.title.title+"</pre>" +
  	  					    		"<b>答案:</b>" +value.title.answer +"<br>");
  	  					    content.appendTo(childdiv);
  	  					    childdiv.appendTo(parentdiv);        
  	  					    parentdiv.appendTo($("#col-list"));
  						});
  						$("#do-collection").show();
  					}
  					else{
  						var content = $("<tr><td>暂无错题</td></tr>");
  						content.appendTo($("#col-list"));
  					}
  			},
  			error:function(){
  				alert("失败");
  			}
  			})
  		}else{
  			location.href = "/account/go_login";
  		}
  	})  
  	
  	
 $(function del(){
	 $("body").on('click',"button[name='del']",function(){
		 var n = $(this).attr("id");
		 console.log(n);
		 var coid = $("input[name='col-id-"+n+"']").attr("value");
		 console.log(coid);
		 $.ajax({
			    url: '/collection/delete/'+coid,
			    type: 'DELETE',
			    success: function(data) {
			    	if(data.tips){
			    		$("#tips").html(data.tips).show();
			    	}else{
			    		$("tr[name='tr-" + n + "']").remove();
			    	}
			    }
			});
	 })
 })
 
 $(function doCol(){
	 $("#do-collection").click(function(){
		 location.href = "/collection/Clist/";
	 });
 })

  	
 