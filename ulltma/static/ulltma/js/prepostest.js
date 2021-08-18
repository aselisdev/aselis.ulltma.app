x = document.getElementsByClassName('tab');

nx = document.getElementById('next');

current = 0;
showtab(current);

function showtab(n){
  x[n].style.display = 'block';
  
  if(!validateForm())
    nx.style.opacity = "0.5";
  else
    nx.style.opacity = "1";

  if (n == 0) {
    document.getElementById("previous").style.display = "none";
  } else {
    document.getElementById("previous").style.display = "inline";
  }
}

function nextprev(n){
  if (validateForm()){
    x[current].style.display = "none";
    current += n;

    if(current >= x.length){
      document.getElementById("prepost").submit();
      return false;
    } 
    showtab(current);
  } else if (n == -1) {
    x[current].style.display = "none";
    current += n;
    showtab(current);
  } else {
    showtab(current);
  }
}

function validateForm(){

  var nonchk = "question_"+(current+1).toString();
  var chk = "question_"+(current+1).toString()+"[]";

  //get the current question
  currques = document.forms["prepost"][nonchk];
  if(currques == null){
    currques = document.forms["prepost"][chk];
  }

  //handle input text boxes
  empty = currques.type === "text" && currques.value === "";

  //supposedly set the value of the HTML checkbox element to a concatenated string of checked values.
  //but it doesn't work for now since HTML reads checkboxes as RADIO button elements. and type is undefined.

  if(empty){
    return false;
  } 

  return true;
}

function validateRadio (radios)
{
  rets = "";
    for (i = 0; i < radios.length; ++ i)
    {
        if (radios [i].checked) rets += radios[i].value;
    }
  return rets;
}