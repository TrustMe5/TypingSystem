function skip(){
pagenum=document.getElementById('pagenum').value;
self.location='/auth/dailypracticeranklist/page='+pagenum;
}
function showclassresult(whichclass){
    self.location='/auth/dailypracticeresultshowByclass/class='+whichclass.value;
}
