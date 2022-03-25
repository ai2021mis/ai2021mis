

// define language reload 
var DataReload = document.querySelectorAll("[data-reload]");
// const reloadbutton = document.querySelector("data-reload");

//translations
var language = {
    eng: {
        welcome: "welcome everyone"
    },
    CN: {
        header_one: "中文yi",
        header_two:"中文 er",
        header_three: "中文 san",
        header_four:"中文si",
        table_trans_one:"中文 tabell",
        table_trans_two:"中文 id",
        table_trans_three:"中文 tabell 3",
        table_trans_four:"中文 tabell 4",
        table_trans_five:"中文 tabell 5",
        translate_table_header: "中文 option",
        translate_table_header_two: "中文 option",
        translate_table_header_three: "中文 option",
        translate_button_one:"中文 button",
        translate_sth:"someeee"
    }
};

//define language with window hash
if (window.location.hash) {
    if (window.location.hash === "#CN"){
        //iki statistik di atas
        type_one.textContent = language.CN.header_one;
        type_two.textContent = language.CN.header_two;
        type_three.textContent = language.CN.header_three;
        type_four.textContent = language.CN.header_four;
        //iki tabel yg ditengah
        table_one.textContent = language.CN.table_trans_one;
        table_two.textContent = language.CN.table_trans_two;
        table_three.textContent = language.CN.table_trans_three;
        table_four.textContent = language.CN.table_trans_four;
        table_five.textContent = language.CN.table_trans_five;

        //iki yg profile di kiri
        header_table_one.textContent = language.CN.translate_table_header;
        header_table_two.textContent = language.CN.translate_table_header_two;
        header_table_three.textContent = language.CN.translate_table_header_three;
        //iki button
        button_id.textContent = language.CN.translate_button_one;
        //coba2
        something.textContent = language.CN.translate_sth;

    }
}

// define language reload onclick.. brati gausa click refresh
for (i = 0; i <= DataReload.length; i++) {
    DataReload[i].onclick = function(){
        location.reload(true)
    };
}



// function reloading(){
//     reloading = location.reload(true);
// }
// reloadbutton.addEventListener("click", reloading);
