function Add_Row(){
    console.log("La fonction est bien appelée")
    }

$( document ).ready(function() {
    // Increment row
    var i = 0;
    function buttonClick() {
        i++;
    };
     //add one row
    let add_row = function() {
      let tbody = $("tbody");
      const row_id = tbody.length + i;
      buttonClick()
      $("tbody").append(`
      <tr id=tr_row_${row_id}>
        <td>${row_id}</td>
        <td><input class='form-control mr-sm-2 input_recipe recipe_input .autocomplete-lunch' placeholder='Faire une recherche' name='lunch' id='lunch${row_id}'></td>
        <td><input class='form-control mr-sm-2 input_recipe recipe_input .autocomplete-supper' placeholder='Faire une recherche' name='supper' id='supper_${row_id}'></td>
        <td><input type="button" class="remove btn btn-outline-secondary" onclick="remove_row(${row_id})" value="Remove"/></td>
      </tr>
      `,
      auto_completion(row_id),
      Add_Row()
      );
    };

    // delete a specific row
    let remove_row = function(row_id) {
      $("#tr_row_"+ row_id).remove();
    };

    
    // create Json with all of the input
    let extract_to_json = function(row_id) {
      console.log("Json crée")
      let results = []
      // console.log($("tr .recipe_input").val());
      // $("tr .recipe_input").each(() =>{ 
      //   console.log($(this).val());
      // });
      $('tr .recipe_input').each(function () {
      
      results.push($(this).val())
      });
      newString = JSON.stringify(results, null, 0)
      console.log(newString)
      // document.getElementById("query").innerHTML = newString;
      return newString
    };

    let print_input = function(){
      $("input#query2").append(newString); 
      console.log("nuk");
    };

   
    let send_json = function(){
      let json_list = extract_to_json()
      console.log(json_list)
      $.ajax({
      type: 'GET',
		  url: "/recipe",
		  data: {
        json_list : newString,
      },
      success: function(data, textStatus, xhr) {
        console.log(xhr.status);
      },
      complete: function(xhr, textStatus) {
        console.log(xhr.status);
      },
		  dataType: "json"
		});
    };

    function auto_completion(row_id){
    $( function() {
        $( ".autocomplete-lunch" ).autocomplete({
        source: "/name_recipe",
        minLength: 3  
        });
        $( ".autocomplete-supper" ).autocomplete({
        source: "/name_recipe",
        minLength: 3
        });
    } );
    };

 });