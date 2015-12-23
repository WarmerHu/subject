  
var jsonData = {};
$(function()
  	{$('#tips').hide();}
  	)
  	
  	$(function(){
  		$.ajax({
  			type:"GET",
  			url:"/elist/1",
  			dataType:"json",
  			success:function(data){
  				$('#title').html(data.title);
  				jsonDate = data;
  			},
  			error:function(){
  				alert("失败");
  			}
  		})
  	})
  	
