var currX = 0;
var currY = 0;
//passes the command typed into the console when the enter key is pressed
document.getElementById("console")
.addEventListener("keyup", function(event) {
event.preventDefault();
    if (event.keyCode === 13) {
        eel.recieve(document.getElementById('console').value, 0);
        document.getElementById('console').value = ""
    }
});
//clears the console input
function clearConsoleInput(){
    document.getElementById('console').value = ""
}
//clears output
function clearConsole(){
    document.getElementById('consoleOutput').value = ""
}
//updates the console output with sent information
eel.expose(update);

function update(data){
    document.getElementsByClassName('block')[0].value =  document.getElementsByClassName('block')[0].value + "\n" + data;
}
//updates the current position to the global values
//the global values are stored in this script to avoid confusion if they were stored in both scripts
eel.expose(updateCurr);
function updateCurr(x , y){
    currX = x;
    currY = y;
}
//draws the visualization of the antenna
eel.expose(draw);
function draw(angle){
    var c = document.getElementById("draw");
    var ctx = c.getContext("2d");
    ctx.clearRect(0, 0, c.width, c.height);
    ctx.save();
    ctx.translate(150, 225)
    ctx.rotate((-1 * angle) * Math.PI / 180);
    ctx.fillStyle = "white"
    ctx.fillRect(0,-40, 130,5);
    ctx.fillRect(5, -40, -5, -40);
    ctx.fillRect(5, -80, 30, 5);
    ctx.fillRect(5, -40, -5, 40);
    ctx.fillRect(0, 0, 35, 5);
    ctx.translate(-150, -225);
    ctx.restore();
}
//funtion for managing the dropdown menus
function drop(id) {
    document.getElementById(id).classList.toggle("show");
}
window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
  
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
          if (openDropdown.classList.contains('show')) {
              openDropdown.classList.remove('show');
          }
        }
      }       
  }     
//returns the current position of the antenna to the python script
eel.expose(returnPos);
function returnPos(){
    return [currX, currY]
}
function blockinput(input){
    if(document.getElementById('toggled').style.display == "none"){
        document.getElementById('console').value = document.getElementById('console').value + input + '\n';
    }else{
        document.getElementById('builder').value = document.getElementById('builder').value  + input + '\n';
  }
}
function minimalView(){
    document.getElementsByClassName('scriptbuilder')[0].style.display ='none';
    document.getElementsByClassName('inputbuttons')[0].style.display ='none';
}
function productiveView(){
    document.getElementsByClassName('scriptbuilder')[0].style.display ='block';
    document.getElementsByClassName('inputbuttons')[0].style.display ='block';
}
function settingsToggle(id){
    if(document.getElementById(id).style.display == "none"){
        document.getElementById(id).style.display = 'block';
        if(id == "lightmode"){
            document.body.style.background = 'rgb(185, 185, 185)'
        }
    }else{
        document.getElementById(id).style.display = 'none';
    if(id == "lightmode"){
        document.body.style.background = 'rgb(34, 34, 34)'
    }
  }
}
function generateScript(){
    eel.generateScript(document.getElementById("builder").value, document.getElementById("visible").value)
}