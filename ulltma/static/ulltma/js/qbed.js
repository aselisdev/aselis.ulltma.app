x = document.getElementsByClassName('tab');

current = 0;
showtab(current);

function showtab(n){
  x[n].style.display = 'block';
  if (n == 0) {
    document.getElementById("previous").style.display = "none";
  } else {
    document.getElementById("previous").style.display = "inline";
  }

  nxt = document.getElementById("next");

  if (n == x.length - 1) {
    nxt.value = "Submit";
  } else {
    nxt.value = "Next";
  }
}

function nextprev(n){
	if(n == 1 && validateForm()){
		x[current].style.display = "none";
		current += n;
		if(current >= x.length){
    		document.getElementById("lassess").submit();
    		return false;
 		}
 		showtab(current);
	} else if (n == -1){
		x[current].style.display = "none";
		current += n;
		showtab(current);
	} 
	else {
		showtab(current);
	}
}

function validateForm() {
  for (var i = 0; i <= 3; i++) {
  	 locstr = "freq_"+(4*current + i).toString();
  	 console.log(locstr);
  	 if(!validateRadio(document.forms["lassess"][locstr])){
  	 	return false;
  	 	break;
  	 }
  }
  return true;
}

function validateRadio (radios)
{
    for (i = 0; i < radios.length; ++ i)
    {
        if (radios [i].checked) return true;
    }
    return false;
}