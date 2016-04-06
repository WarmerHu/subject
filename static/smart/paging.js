pageCount = 1;
curPage = 1;
function paging(num,pardiv){
	if(num<25){
		for(var i=1;i<=num;i++){
			$('<li><a href="#" class="ap" name="p" id="p-'+i+'">'+i+'</a></li>').appendTo($(pardiv));
		}
	}else{
		for(var i=1;i<25;i++){
			$('<li><a href="#" name="p" class="ap" id="p-'+i+'">'+i+'</a></li>').appendTo($(pardiv));
		}
		$('<li><a href="#" class="ap" name="pelse" id="p-'+(i+1)+'">...</a></li>').appendTo($(pardiv));
	}
	$('<li><a href="#" class="ap" name="next"><span aria-hidden="true">&raquo;</span></a></li>').appendTo($(pardiv));
}
function changeColor(elem){
	$('.ap').attr("style","background-color:#fff");
	$('#p-'+curPage).attr("style","background-color:#337ab7");
}
$(function(){
	$("body").on('click',".ap",function(){
		name = $(this).attr("name");
		if(name=='pre'){
			if(curPage>1){
				curPage -= 1;
				showData(curPage);
				changeColor(curPage);
			}
		}else if(name=='next'){
			if(curPage<pageCount){
				curPage += 1;
				showData(curPage);
				changeColor(curPage);
			}
		}else if(name=='p'){
			curPage = parseInt($(this).html());
			showData(curPage);
			changeColor(curPage);
		}else{
			
		}
	});
})