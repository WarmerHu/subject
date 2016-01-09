
	$(function(){
  		if($.cookie("username")){
  			console.log("退出登录");
  			$("#islog").html("退出登录");
  			$("#reallog").html($.cookie("username"));
  			$("#islog").attr("href","/account/logout");
  			$.ajax({
  				type:"GET",
  				url:"/resources/list",
  				dataType:"json",
  				success:function(data){
  					if(!$.isEmptyObject(data)){
  						console.log("data:",data);
  						$.each(data,function(n,value){
  	  						var parentdiv=$("<tr name='tr-" + n + "'></tr>");  
  	  					    var name=$("<td>"+
  	  					    	"<input type='hidden' name='col-id-"+ n +"' value=" + value.id + ">" + 
	  					    	"<input type='hidden' name='col-up-id-"+n+ "' value=" + value.uploader + ">" +
  	  					    	value.downloader.split("/").pop() +"</td>");   
  	  					    var money=$("<td>"+value.money+"</td>");   
  	  					    var downloaded=$("<td>"+value.downloaded+"</td>");   
  	  					    var downloader=$("<td>"+value.downloader+"</td>");   

  	  					    name.appendTo(parentdiv);        
  	  					    money.appendTo(parentdiv);        
  	  					    downloaded.appendTo(parentdiv);        
  	  					    downloader.appendTo(parentdiv);        
  	  					    parentdiv.appendTo($("#col-list"));
  						});
  					}
  					else{
  						var content = $("<tr><td>暂无资源</td><td></td><td></td><td></td></tr>");
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
  	
  	
 $(function(){
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

  	
 