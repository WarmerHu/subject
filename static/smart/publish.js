  
dataId = "";
dataVal = []
 
function firt(){
	$(".form-control").removeAttr("readonly");
	$("#excecl-up").hide();
	$("#add-val").removeAttr("disabled");
}
function sect(){
	$(".form-control").attr("readonly","true");
	$("#excecl-up").show();
	$("#add-val").attr("disabled","true");
}

$(function initail(){
	$("#excecl-up").hide();
	addData() ;
	nextData();
})
function nextData(){
	 $("#add-val").click(function(){
		 $("#tips").html("").hide();
		 title = $("textarea[name='question']").val().trim();
		 answer = $("input[name='answer']").val().trim();
		 tips = $("input[name='hint']").val().trim();
		 if(!title || !answer){
			 $("#tips").html("请输入正确的题目&答案").show();
		 }
		 else{
			 dataVal.push({"title":title,"answer":answer,"tips":tips});
			 $("#tips").html("直接输入下一题，已输入所有题目请点击'保存'").show();
			 $("textarea[name='question']").val('');
			 $("input[name='answer']").val('');
			 $("input[name='hint']").val('');
		 }
	 })
 }
function doUpload(){
	var file = $("#uploadedfile").val();
	var strFileName=file.split("/").pop();
	$("#filename").val(strFileName);
	var formData = new FormData($( "#uploadForm" )[0]);  
     $.ajax({  
          url: '/title/publish/?p=upload' ,  
          type: 'POST',  
          data: formData,  
          async: false,  
          cache: false,  
          contentType: false,  
          processData: false,  
          success: function (data) {  
        	  $("#tips").html(data.tips).show();
          },  
          error: function () {  
        	  alert("保存失败"); 
          }  
     }); 
}

function addData() {
  	$("#sub-val").click(function() {
  		if($("#add-val").attr("disabled")){
  			doUpload();
  		}else{
  			title = $("textarea[name='question']").val().trim();
  			 answer = $("input[name='answer']").val().trim();
  			 tips = $("input[name='hint']").val().trim();
  			 if(!title || !answer || $.isEmptyObject(dataVal)){
  				 $("#tips").html("请输入正确的题目&答案").show();
  			 }
  			 else{
  				 dataVal.push({"title":title,"answer":answer,"tips":tips});
  			 }
  				
  			if(!$.isEmptyObject(dataVal)){
  				$.ajax({
			        type: "POST",
			        url: "/title/publish/?p=input",
			        dataType: "json",
			        timeout: 1000,
			        data:JSON.stringify(dataVal),
			        error: function(){
			        	alert("保存失败");
			        },
			        success: function(data){
			        	$("#tips").html(data.tips).show();
			        	title = $("textarea[name='question']").val("");
			   		 	answer = $("input[name='answer']").val("");
			   		 	tips = $("input[name='hint']").val("");
			   		 	dataVal = [];
			        }
  				})
  			}
  		}
	})
}