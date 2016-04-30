pageCount2 = 1;
curPage2 = 1;
function paging2(num,pardiv){
	if(num<25){
		for(var i=1;i<=num;i++){
			$('<li><a href="#" class="ap2" name="p" id="p2-'+i+'">'+i+'</a></li>').appendTo($(pardiv));
		}
	}else{
		for(var i=1;i<5;i++){
			$('<li><a href="#" name="p2" class="ap2" id="p2-'+i+'">'+i+'</a></li>').appendTo($(pardiv));
		}
		$('<li><a href="#" class="ap2" name="pelse" id="p2-'+(i+1)+'">...</a></li>').appendTo($(pardiv));
	}
	$('<li><a href="#" class="ap2" name="next"><span aria-hidden="true">&raquo;</span></a></li>').appendTo($(pardiv));
}
function changeColor2(elem){
	$('.ap2').attr("style","background-color:#fff");
	$('#p2-'+curPage2).attr("style","background-color:#337ab7");
}
$(function(){
	$("body").on('click',".ap2",function(){
		name = $(this).attr("name");
		console.log(name);
		console.log(curPage2);
		if(name=='pre'){
			if(curPage2>1){
				curPage2 = parseInt(curPage2);
				curPage2 -= 1;
				showData2(curPage2);
				changeColor2(curPage2);
			}
		}else if(name=='next'){
			if(curPage2<pageCount2){
				curPage2 = parseInt(curPage2);
				curPage2 += 1;
				showData2(curPage2);
				changeColor2(curPage2);
			}
		}else if(name=='p'){
			curPage2 = parseInt($(this).html());
			showData2(curPage2);
			changeColor2(curPage2);
		}else{
			
		}
	});
})
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

function showData(p){
	$("#o-all").children().remove();
	$.ajax({
		type:"GET",
		url:"/account/opinion/?p="+p+"&e=5",
		success:function(data){
			if(!$.isEmptyObject(data)){
				if(data.numT){
					pageCount = Math.ceil(data.numT / 5);
					paging(pageCount,"#pagination1");
				}
				$.each(data.opinion,function(n,v){
					var topic = $("<tr class='toTopic' id='"+v.topicId+"'>" +
							"<td>"+v.topicName+"</td>" +
									"<td>"+v.time+"</td></tr>");
					topic.appendTo($("#o-all"));
				});
			}
		}
	});
}

function showData2(p){
	$("#t-all").children().remove();
	$.ajax({
		type:"GET",
		url:"/account/topic/?p="+p+"&e=5",
		success:function(data){
			if(!$.isEmptyObject(data)){
				if(data.numT){
					pageCount2 = Math.ceil(data.numT / 5);
					paging2(pageCount2,"#pagination2");
				}
				$.each(data.topic,function(n,v){
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
	showData2(0);
	showData(0);
//	page();
	$("#PWch").hide();
	$("#tips").hide();
	$("#error").hide();
	$("#change-head").hide();		
 	changePW();
}) 




