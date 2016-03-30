function ifcanenter(whichcontext){
var start_time=whichcontext.parentNode.parentNode.getElementsByTagName('td')[2].firstChild.nodeValue;
var end_time=whichcontext.parentNode.parentNode.getElementsByTagName('td')[3].firstChild.nodeValue;
start_time=parseInt(start_time.match(/\d/g).join(""));
end_time=parseInt(end_time.match(/\d/g).join(""));
var current_time=parseInt((document.getElementById('current_time').firstChild.nodeValue).match(/\d/g).join(""));
if(start_time>current_time){
alert('请注意比赛开始时间！');
}
else{
self.location='/auth/context_show/context_id='+whichcontext.parentNode.parentNode.getElementsByTagName('td')[0].firstChild.nodeValue;
}
}
