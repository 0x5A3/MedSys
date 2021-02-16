const login = () => {
    let username = input_get($("#username"));

    request("POST", "$login", 
        { 
            username: username, 
            password: input_get($("#password"))
        },
        data => { 
            if(!data.success){
                $("#password").childNodes[2].innerHTML = data.reason;
            }
            else{
                goto(`store/${username}/`);
            }
        }
    );
};