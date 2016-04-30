function initial(){
  		$.ajax({
				type:"GET",
				url:"/jobs/list",
				dataType:"json",
				success:function(data){
					if(!$.isEmptyObject(data)){
						$.each(data,function(n,value){
	  						var jdiv=$("<div class='jp' id="+n+">"+value.positon+"("+value.company+"-"+value.createtime+")</div>");
	  						var jddiv = $("<div class="+n+">"+value.duty+"<br/>联系方式："+value.contact
	  								+"&nbsp&nbsp&nbsp来源："+value.source+"</div>");
	  						jddiv.hide();
	  						var jadiv = $("<div></div>")
	  						jdiv.appendTo(jadiv);
	  						jddiv.appendTo(jadiv);
	  						jadiv.appendTo($("#ls"));
						});
					}
					else{
						var content = $("暂无职位");
						content.appendTo($("#ls"));
					}
			},
			error:function(){
				$("#tips").html("获取职位列表失败");
			}
			});
}
 
function fol(){
    $("body").on('click',$(".jp"),function(){
    	$("div[class="+this.attr('id')+"]").toggle();
    });
}

$(function(){
	initial();
	fol();
})
