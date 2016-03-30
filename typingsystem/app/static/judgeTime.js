function text(){
var starttime=document.getElementById('timeaction').value+" "+document.getElementById("starthour").value+":"+document.getElementById('startmins').value+':00';
var endtime=document.getElementById('timeover').value+" "+document.getElementById("endhour").value+":"+document.getElementById('endmins').value+':00';
if(parseInt(starttime.match(/\d/g).join(""))>=parseInt(endtime.match(/\d/g).join(""))){
alert('开始时间要小于结束时间！');
}
}

function submt(){
var starttime=document.getElementById('timeaction').value+" "+document.getElementById("starthour").value+":"+document.getElementById('startmins').value+':00';
var endtime=document.getElementById('timeover').value+" "+document.getElementById("endhour").value+":"+document.getElementById('endmins').value+':00';
document.getElementById('articlename').value=document.getElementById('sect').value;
document.getElementById('start_time').value=starttime;
document.getElementById('end_time').value=endtime;
}
