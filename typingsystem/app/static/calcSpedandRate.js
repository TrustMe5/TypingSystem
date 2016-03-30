var c=0;
var t;
function timedCount(){
if(c>=60){
    var mins=parseInt(c/60);
    var secd=c-60*mins;
    document.getElementById('time_input').value=mins+"分"+secd+'秒';
}else{
document.getElementById('time_input').value=c+'秒';
}
c=c+1;
t=setTimeout("timedCount()",1000);
r=setTimeout("spedandrate()",1000);
}
function spedandrate(){
     var greennum=document.getElementsByClassName('green').length;
     var rednum=document.getElementsByClassName('red').length;
     var sum=((greennum+rednum)/c*60).toFixed(2);
     document.getElementById('speedshow').setAttribute('value',sum+"KPM");
     if(greennum+rednum==0){
     document.getElementById('accuracy_rate').setAttribute('value',"0%");     
     }else{
     var correctrate=(greennum/(greennum+rednum)*100).toFixed(2);
     document.getElementById('accuracy_rate').setAttribute('value',correctrate+"%");     
}
}
