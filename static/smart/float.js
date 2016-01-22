function menuFixed(id){
    var obj = document.getElementById(id);
    var _getHeight = obj.offsetTop; //offsetTop:获取对象相对于版面或由 offsetTop 属性指定的父坐标的计算顶端位置
    
    window.onscroll = function(){ //onscroll:滚动div时的事件
        changePos(id,_getHeight);
    }
}
function changePos(id,height){
    var obj = document.getElementById(id);
    var scrollTop = document.documentElement.scrollTop || document.body.scrollTop;	//获取滚动条的滚动距离
    if(scrollTop < height){
        obj.style.position = 'relative';
        obj.style.top = '0px';
    }else{
        obj.style.position = 'fixed';
        obj.style.top = '50px';
    }
}

window.onload = function(){
    menuFixed('nav');
}