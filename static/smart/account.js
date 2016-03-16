function get_base(){
	$.ajax({
		type:"GET",
		url:"/account/list",
		success:function(data){
			if(!$.isEmptyObject(data)){
				var base = $("<div>用户名："+data.name+
						"<br/>邮箱:"+data.email+
						"<br/>积分："+data.point+"</div>");
				base.appendTo($("#na-e-p"));
				
				var img = $("<img src='"+data.head+"'class='img-polaroid'>");
				img.appendTo($(".thumbnail"));
			}
		}
	});
}

function get_opinion(){
	$.ajax({
		type:"GET",
		url:"/account/opinion",
		success:function(data){
			if(!$.isEmptyObject(data)){
				$.each(data,function(n,v){
					var topic = $("<tr class='toTopic' id='"+v.topicId+"'>" +
							"<td>"+v.topicName+"</td>" +
									"<td>"+v.time+"</td></tr>");
					topic.appendTo($("#o-all"));
				});
			}
		}
	});
}

function get_topic(){
	$.ajax({
		type:"GET",
		url:"/account/topic",
		success:function(data){
			if(!$.isEmptyObject(data)){
				$.each(data,function(n,v){
					var topic = $("<tr class='toTopic' id='"+v.topicId+"'>" +
							"<td>"+v.topicName+"</td>" +
									"<td>"+v.time+"</td></tr>");
					topic.appendTo($("#t-all"));
				});
			}
		}
	});
}

$(function(){
	$("body").on('click',"tr[class='toTopic']",function(){
		$.cookie("bbsid",$(this).attr("id"),{path:"/bbs/"});
		location.href = "/bbs/topic";
	});
    
	$("body").on('click',"img[class='img-polaroid']",function(){
		$("#change-head").show();
	});
})
function changePW(){
	$("#sub").click(function(){
			$("#PWch").toggle();
	})
}

function doUpload(){
	var file = $("#uploadedfile").val();
	var strFileName=file.split("/").pop();
	$("#filename").val(strFileName);
	var formData = new FormData($( "#uploadForm" )[0]);  
     $.ajax({  
          url: '/account/picture/' ,  
          type: 'POST',  
          data: formData,  
          async: false,  
          cache: false,  
          contentType: false,  
          processData: false,  
          success: function (data) {  
        	  $("img[class='img-polaroid']").attr("src",data.head);
        	  $("#change-head").hide();	
          },  
          error: function () {  
        	  $("#tips").html("上传失败").show();  
          }  
     }); 
}

$(function check(){
	$("#sub-val").click(function(){
		var usps = $.trim($("input[name='password']").val());
		var usre = $.trim($("input[name='re_password']").val());
		var uso = $.trim($("input[name='oldpassword']").val());
		
		if(uso.length<6 || uso.length>20 || usps.length<6 || usps.length>20 || !usps || !uso){
			$("#error").html("请输入正确的新旧密码").show();
		}
		else if(usps!=usre){
			$("#error").html("确认密码错误").show();
		}
		else if(uso == usps){
			$("#error").html("新旧密码相同").show();
		}
		else{
			$.ajax({
				type:"POST",
				url:"/account/ps/",
				dataType:"json",
				data:JSON.stringify({
					'oldps':$.md5(uso),
					'newps':$.md5(usps)
				}),
				success:function(result){
					$("#error").html(result.error).show();
				},
				error:function(result){
					$("#error").html("请求错误").show();
				}
			});
		}
	})
})

function page(){
	var show_per_page = 3; 
	var number_of_items = $('#t-all').children().size();
	var number_of_pages = Math.ceil(number_of_items/show_per_page);
	console.log(number_of_items);
	console.log(number_of_pages);
	$('#current_page').val(0);
	$('#show_per_page').val(show_per_page);
	var navigation_html = '<a class="previous_link" href="javascript:previous();">Prev</a>';
	var current_link = 0;
	while(number_of_pages > current_link){
		navigation_html += '<a class="page_link" href="javascript:go_to_page(' + current_link +')" longdesc="' + current_link +'">'+ (current_link + 1) +'</a>';
		current_link++;
	}
	navigation_html += '<a class="next_link" href="javascript:next();">Next</a>';
	$('#page_navigation').html(navigation_html);
	$('#page_navigation .page_link:first').addClass('active_page');
	$('#t-all').children().css('display', 'none');
	$('#t-all').children().slice(0, show_per_page).css('display', 'block');	
}

$(function initial(){
	get_base();
	get_topic();
	get_opinion();
	page();
	$("#PWch").hide();
	$("#tips").hide();
	$("#error").hide();
	$("#change-head").hide();		
 	changePW();
}) 




