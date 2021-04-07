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
  currques = document.forms["prepost"]["question_"+(current+1).toString()];

  //handle input text boxes
  empty = currques.type === "text" && currques.value === "";

  //handle radios
  st = currques.toString();
  str = st.replace("[", "");
  stri = str.replace("]", "");

  unchecked = stri.split(" ")[1] === "RadioNodeList" && !validateRadio(currques);

  if(empty){
    return false;
  } else if (unchecked){
    return false;
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