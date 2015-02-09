function is_valid(string,regex){
	return !(!(string.match(regex)))
}

function check_all_inputs(){
	var error_count = 0;
	error_count += check_input($("#input_name").val(),"#error_event_name",'^[a-zA-Z0-9_]*$');
	error_count += check_input($("#input_name").val(),"#error_venmo_id",'^[0-9_]*$');
	error_count += check_input($("#input_email").val(),"#error_email","^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$");
	error_count += check_input($("#input_rec_amt").val(),"#error_rec_amount","^[0-9]*$");
	if (error_count > 0) alert("Invalid inputs!");
}

function raise_error(error_id){
	
	$( error_id ).html("Invalid input");
}
function remove_error(error_id){
	$( error_id ).html("");	
}

function check_input(input,error_id,regex){
	valid = 0;
	if (input != ""){
		if (is_valid(input,regex)){
			valid = 0;
		} else {
			valid = 1;
		}
	} else {
		valid = 1;
	}
	remove_error(error_id);
	if (valid){
		raise_error(error_id);
	}
	return valid;
}

$( document ).ready(function(){
	$('#input_id').change(function(){
		check_input($( this ).val(),"#error_venmo_id","^[0-9]*$");
	});
	$('#input_email').change(function(){
		check_input($( this ).val(),"#error_email","^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$");
	});
	$('#input_rec_amt').change(function(){
		check_input($( this ).val(),"#error_rec_amount","^[0-9]*$");
	});
	$('#input_date').change(function(){
		check_input($( this ).val(),"#error_end_date","^[0-9]+\-+[0-9]+\-+[0-9]+$");
	});
});

