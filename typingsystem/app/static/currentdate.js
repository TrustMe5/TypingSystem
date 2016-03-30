function startTime()
{
    var today=new Date()
        var year=today.getFullYear()
        var month=today.getMonth()+1
        var day=today.getDate()
        var h=today.getHours()
        var m=today.getMinutes()
        var s=today.getSeconds()
        // add a zero in front of numbers<10
        if (month >= 1 && month <= 9) {
                    month = "0" + month;
                        }
        if (day >= 0 && day <= 9) {
                    day = "0" + day;
                        }
        h=checkTime(h)
        m=checkTime(m)
        s=checkTime(s)
        document.getElementById('current_time').innerHTML=year+"-"+month+"-"+day+" "+h+":"+m+":"+s
        t=setTimeout('startTime()',500)
}

function checkTime(i)
{
    if (i<10) 
          {i="0" + i}
      return i
}

