window.onload=function(){
    {% if not writer %}
    document.getElementById('iflogin').innerHTML="<a href='/auth/login'>登陆</a> ";
    self.location='/auth';
    {%else%}
    document.getElementById('iflogin').innerHTML="<a href='/auth/homepage/user={{writer}}'>当前用户:{{writer}}</a>";
    document.getElementById('add').innerHTML="<a href='/auth/addcontext'>添加比赛</a>";
    {%endif%}
}
