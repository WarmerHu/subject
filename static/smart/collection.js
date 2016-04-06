function showData(p){
	$("#col-list").children().remove();
	$.ajax({
			type:"GET",
			url:"/collection/list/?p="+p,
			dataType:"json",
			success:function(data){
				if(!$.isEmptyObject(data)){
					if(data.numT){
						pageCount = Math.ceil(data.numT / 20);
						paging(pageCount,".pagination");
					}
					$.each(data.col,function(n,value){
						var parentdiv=$("<tr name='tr-" + n + "'></tr>");  
					    var childdiv=$('<td></td>');   
					    var content = $(
					    		"<input type='hidden' name='col-id-"+ n +"' value=" + value.id + ">" + 
					    		"<input type='hidden' name='col-title-id-"+n+ "' value=" + value.title.id + ">" +
					    		"<a href='#' name='del' id='" + n + "'><span class='glyphicon glyphicon-remove' aria-hidden='true'></span></a>" +
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
}

	$(function initial(){
		$("#do-collection").hide();
		$("#tips").hide();
  		showData(0);
  	})  
  	
  	
 $(function del(){
	 $("body").on('click',"a[name='del']",function(){
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

  	
 