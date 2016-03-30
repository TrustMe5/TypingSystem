function spedandrate(){
    //alert(document.getElementById('div3').lastChild.nodeValue.length);
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
