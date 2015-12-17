$(function() {
		$("#sub-val").click(function() {
			if({{rsp.answer}}==$('#sub-ans').val()){
				$.ajax({
			        type: 'GET',
			        url: '/elist/{{rsp.id}}+1',
//			        获取返回的json
//			        将数据放入title中
//			        清空answer输入框
			      });
			 }
		})
	})