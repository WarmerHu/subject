  
dataId = "";
dataVal = []
	$(function(){
		$("#tips").hide();
  		if($.cookie("username")){
  			$("#islog").html("退出登录");
  			$("#reallog").html($.cookie("username"));
  			$("#islog").attr("href","/account/logout");
  		}else{
  			location.href = "/account/go_login";
  		}
  	})  

  	
 $(function nextData(){
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
		 }
	 })
 })
  	
  	$(function addData() {
  		$("#sub-val").click(function() {
  			title = $("textarea[name='question']").val().trim();
  			 answer = $("input[name='answer']").val().trim();
  			 tips = $("input[name='hint']").val().trim();
  			 if(!title || !answer){
  				 $("#tips").html("请输入正确的题目&答案").show();
  			 }
  			 else{
  				 dataVal.push({"title":title,"answer":answer,"tips":tips});
  			 }
  				
  			if(dataVal){
  				console.log(JSON.stringify(dataVal));
  				$.ajax({
			        type: "POST",
			        url: "/title/publish/",
			        dataType: "json",
			        timeout: 1000,
			        data:JSON.stringify(dataVal),
			        error: function(){
			        	alert("保存失败");
			        },
			        success: function(data){
			        	$("#tips").html("已保存").show();
			        	title = $("textarea[name='question']").val("");
			   		 answer = $("input[name='answer']").val("");
			   		 tips = $("input[name='hint']").val("");
			        }
  				})
  			}else{
  				$("#tips").html("请正确输入题目&答案").show();
  			}
	}
  			  )
  	})