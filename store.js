let cart = {};

const add_item_quantity = (elem, id, checkout) => {
    add_item(elem.nextSibling, id, checkout);
}
const add_item = (elem, id, checkout = false) => {
    request("POST", "/$cart_add", 
        { 
            "username": username,
            "item_id": id,
            "quantity": elem.previousSibling.value
        },
        data => {
            if(data.success){
                elem.value = "Remove";
                elem.onclick = () => remove_item(elem, id, checkout);  
                
                if(checkout){
                    goto_checkout();
                }
            }
            else{
                alert(data.reason);
            }
        }     
    );
};
const remove_item = (elem, id, checkout = false) => {
    request("POST", "/$cart_remove", 
        { 
            "username": username,
            "item_id": id 
        },
        data => {
            if(data.success){
                elem.previousSibling.value = 0;
                elem.value = "Add to cart";
                elem.onclick = () => add_item(elem, id, checkout);

                if(checkout){
                    goto_checkout();
                }
            }
            else{
                alert(data.reason);
            }
        }     
    );
};
const checkout_remove = (elem, id) => {
    request("POST", "/$cart_remove", 
        { 
            "username": username,
            "item_id": id 
        },
        data => {
            if(data.success){
                goto_checkout();
            }
            else{
                alert(data.reason);
            }
        }     
    );
};
const purchase = () => {
    request("POST", "/$purchase", 
        { 
            username: username,
            address: input_get($("#address"))
        },         
        data => {
            if(data.success){
                goto_store();
            }
            else{
                alert(data.reason);
            }
        }     
    );
}

const search = elem => {
    if(event.key == "Enter"){
        const query = elem.value;

        goto(`${query}`);
    }
};

const goto_store = () => { goto(`/store/${username}/`); }
const goto_checkout = () => { goto(`/checkout/${username}`); }