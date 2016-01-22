	$(function initial(){
  		$.ajax({
				type:"GET",
				url:"/resources/list",
				dataType:"json",
				success:function(data){
					if(!$.isEmptyObject(data)){
						$.each(data,function(n,value){
	  						var parentdiv=$("<tr name='tr-" + n + "'></tr>");  
	  					    var name=$("<td>"+
	  					    	"<input type='hidden' name='col-id-"+ n +"' value=" + value.id + ">" + 
  					    	"<input type='hidden' name='col-up-id-"+n+ "' value=" + value.uploader + ">" +
	  					    	value.downloader +"</td>");   
	  					    var money=$("<td name='p-"+n+"'>"+value.money+"</td>");   
	  					    var downloaded=$("<td id='"+value.id+"-count'>"+value.downloaded+"</td>");   
	  					    var downloader=$("<td><button class='btn btn-link' id="+n+" value='"+value.downloader+"'>下载</a></td>");   

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
				alert("获取资源列表失败");
			}
			});
  	})  
  

  	
function doUpload(){
		var file = $("#uploadedfile").val();
		var strFileName=file.split("/").pop();
		$("#filename").val(strFileName);
		var formData = new FormData($( "#uploadForm" )[0]);  
	     $.ajax({  
	          url: '/resources/upload/' ,  
	          type: 'POST',  
	          data: formData,  
	          async: false,  
	          cache: false,  
	          contentType: false,  
	          processData: false,  
	          success: function (data) {  
	              $("#tips").html(data.tips).show();  
	          },  
	          error: function (data) {  
	        	  $("#tips").html("上传失败").show();  
	          }  
	     }); 
	}
 
	 $(function download(){
		 $("body").on('click',"button[class='btn btn-link']",function(){
			 var n = $(this).attr("id");
			 var value = $(this).val();
			 var points = $("td[name='p-"+n+"']").text();
			 var uploader = $("input[name='col-up-id-"+ n +"']").val();
			 var resourceID = $("input[name='col-id-"+ n +"']").val();
			 $.ajax({
					url:"/resources/download/",
					type:"POST",
					dataType: "json",
					timeout: 1000,
					data:{
							"points":points,
							"uploader":uploader,
							"resourceID":resourceID,
					},
			        success: function(data){
			        	if(data.tips){
			        		$("#tips").html(data.tips).show();
			        	}else{
			        		$("#"+data.resourceID+"-count").html(data.count).show();
			        		$("#tips").html("扣除"+points+"积分").show();
			        		location.href = "/media/"+value;
			        	}
			        }
				});
		 })
	 })
	 
