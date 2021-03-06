function Add_Row(){
    console.log("La fonction est bien appelée")
    $("#table_recipe").append("<tr><td>3</td><td><input class='form-control mr-sm-2' placeholder='Faire une recherche' name='query' id='query'></td><td><input type='text' id='name' name='name' requiredminlength='4' maxlength='60' size='40'></td</tr>"); 
}

// document.getElementById("demo").innerHTML =
// obj.employees[1].firstName + " " + obj.employees[1].lastName;

// console.log(JSON.stringify)