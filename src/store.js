let cart = {};

const item_updater = (update, checkout) => () => {
    update();
    if(checkout){ goto_checkout(); }
};

const check_quantity = elem => {
    if(elem.value.length > 0){
        let [v, _min, _max] = [parseInt(elem.value), 
            elem.getAttribute("min"), 
            elem.getAttribute("max")
        ];

        if(v < _min){ v = _min; }
        else if(v > _max){ v = _max; } 
        elem.value = v;    
    }
    else {
        elem.value = 1;
    }
}
const add_item_quantity = (elem, id, checkout) => 
    add_item(elem.nextSibling, id, checkout);
    
const add_item = (elem, id, checkout = false) => {
    check_quantity(elem.previousSibling);
    user_upload("/$cart_add", 
        { 
            item_id: id,
            quantity: elem.previousSibling.value
        },
        item_updater(() => { 
            elem.previousSibling.disabled = false;

            elem.value = "Remove"; 
            elem.onclick = () => remove_item(elem, id, checkout)
        })    
    );
}

const remove_item = (elem, id, checkout = false) =>
    user_upload("/$cart_remove", { item_id: id },
        item_updater(() => {
            elem.previousSibling.value = 0;
            elem.previousSibling.disabled = true;
            
            elem.value = "Add to cart";
            elem.onclick = () => add_item(elem, id, checkout);
        })
    );

const checkout_remove = (elem, id) =>
    user_upload("/$cart_remove", 
        { item_id: id }, goto_checkout);

const purchase = () =>
    user_upload("/$purchase", 
        { address: input_get($("#address")) }, goto_store);

const search = elem => {
    if(event.key == "Enter"){ goto(`${elem.value}`); }
};

const goto_store = () => { goto(`/store/${username}/`); };
const goto_checkout = () => { goto(`/checkout/${username}`); };