function showData(p){
	$("#col-list").children().remove();
	$.ajax({
		type:"GET",
		url:"/resources/list/?p="+p,
		dataType:"json",
		success:function(data){
			if(!$.isEmptyObject(data)){
				if(data.numT){
					pageCount = Math.ceil(data.numT / 20);
					paging(pageCount,".pagination");
				}
				$.each(data.res,function(n,value){
						var parentdiv=$("<tr name='tr-" + n + "'></tr>");  
					    var name=$("<td>"+
					    	"<input type='hidden' name='col-id-"+ n +"' value=" + value.id + ">" + 
				    	"<input type='hidden' name='col-up-id-"+n+ "' value=" + value.uploader + ">" +
					    	value.downloader +"</td>");   
					    var money=$("<td name='p-"+n+"' class='md' >"+value.money+"</td>");   
					    var downloaded=$("<td id='"+value.id+"-count' class='md'>"+value.downloaded+"</td>");   
					    var downloader=$("<td class='md'><a class='dwl' id="+n+" value='"+value.downloader+"' href='/resources/download/?rs="+value.id+"'>下载</a></td>");
					    if(value.complaint){
					    	var complaint=$("<td class='md'><button class='btn btn-link com' id='' au='"+value.uploader+"' rs='"+value.id+"' dw='' cc='can'>取消投诉</button></td>");
					    }else if(value.dw){
					    	var complaint=$("<td class='md'><button class='btn btn-link com' id='' au='"+value.uploader+"' rs='"+value.id+"' dw='true' cc='add'>投诉</button></td>");   
					    }else{
					    	var complaint=$("<td class='md'><button class='btn btn-link com' id='' au='"+value.uploader+"' rs='"+value.id+"' dw='' cc='add'>投诉</button></td>");
					    }
					    name.appendTo(parentdiv);        
					    money.appendTo(parentdiv);        
					    downloaded.appendTo(parentdiv);        
					    downloader.appendTo(parentdiv);        
					    complaint.appendTo(parentdiv);        
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
}
function addComplaintT(that){
	content = 	$.trim($('textarea[name="reason"]').val());
	if(!content || content.length<10){
		alert("请正确输入投诉理由");
	}else{
		jsonData = {
				'content':content
		}
		value = $('input:radio[name="radio"]:checked').val();
		if(value=='resourse'){
			jsonData['rsid'] = parseInt($(that).attr("rs"));
		}else if(value=='author'){
			jsonData['authorid'] = parseInt($(that).attr("au"));
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
	        	if(data.tips){
	        		alert(data.tips);
	        	}else{
	        		$(that).html("取消投诉");
	        		$(that).attr("cc","can");
	        		$("#CMs").hide();
	        	}
	        }
			});
	}
}
function cancelComplaintT(that){
 	rs = parseInt($(that).attr("rs"));
	jsonData = {};
	jsonData['rsid'] = rs;
	$.ajax({
        type: "POST",
        url: "/complaint/cancel/",
        dataType: "json",
        timeout: 1000,
        data:JSON.stringify(jsonData),
        error: function(){
        	alert("取消投诉失败");
        },
        success: function(data){
        	if(data.tips){
        		alert(data.tips);
        	}else{
        		$(that).html("投诉");
        		$(that).attr("cc","add");
        		}
        }
		});
}  
$(function initial(){
  	showData(0);
  	$('#change-head').hide();
  	$("#CMs").hide();
  	 $("body").on('click',".com",function(){
  		 str = $(this).attr("cc");
  		 if(str=='add'){
  			$("#RULE").hide();
//  			if($(this).attr("dw") == "true"){
  				$("#resourse").prop("checked","checked");
  				$(".submitT").attr("rs",$(this).attr("rs"));
  				$(".submitT").attr("au",$(this).attr("au"));
  				$("#CMs").toggle();
  				$(".submitT").click(function(){
  					addComplaintT(this);
  				});
//  			}else{
//  			 alert("假如你没有下载这份资源，你怎么知道资源的内容违反礼仪？");
//  			}
  		}else if(str=='can'){
  			cancelComplaintT(this);
  		}
  	 }) 
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
	              window.location.reload();//刷新当前页面
	          },  
	          error: function (data) {  
	        	  $("#tips").html("上传失败").show();  
	          }  
	     }); 
	}
 /*
	 $(function download(){
		 $("body").on('click',".dwl",function(){
			 var n = $(this).attr("id");
			 var value = $(this).val();
			 var points = $("td[name='p-"+n+"']").text();
			 var uploader = $("input[name='col-up-id-"+ n +"']").val();
			 var resourceID = $("input[name='col-id-"+ n +"']").val();
			 var that = this;
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
			        		location.href = data.dURL;
			        		$(that).parent().next().children(".com").attr("dw","true");
			        	}
			        }
				});
		 })
	 })
	 */
	 
