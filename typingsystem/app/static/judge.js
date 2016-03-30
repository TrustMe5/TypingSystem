      var fLen=0;
    function CheckInput(currid){
         var wrstr=document.getElementById('writing'+currid).value;
        var str=document.getElementById('show'+currid).value;
         var len=wrstr.length;
        var  elem=document.getElementById('div'+currid);

        var divlen=elem.innerHTML.length;
         var dis=str.length;
        var dataset=new Array();
        var mystr=new Array();
           if(len<=dis) {
               for(var i=0;i<len;i++){
               if (wrstr[i] != str[i]) {
                   dataset[i]=1;
               }else {
                   dataset[i]=0;
               }
           }
               for(i=0;i<str.length;i++)
               {
                   mystr[i]=str[i];
               }
                elem.innerHTML=SetDIV(dataset,mystr);
           }else {
              var pos=  currid+1;
               document.getElementById("writing"+currid).value= document.getElementById("writing"+currid).value.substr(0,len-1);
              document.getElementById("writing"+pos).focus();

           }
    }
    function SetDIV(DataSet,MyStr){

        for(var i=0;i<DataSet.length;i++)
        {

            if(DataSet[i]==1)
            MyStr[i]='<span  class="red">'+MyStr[i]+'</span>';
             if(DataSet[i]==0)
            MyStr[i]='<span  class="green">'+MyStr[i]+'</span>';
        }
       var HTStr="";
        for ( var i=0;i<MyStr.length;i++)
        {
            HTStr+=MyStr[i];
        }
      return HTStr;
    }
