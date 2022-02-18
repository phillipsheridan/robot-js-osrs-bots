/* 

TODO

add TS support
make inputs passable from command line or let the use click where they want instead of finding own positions

*/

var robot = require("robotjs");

// todo use args

const args = process.argv.slice(2);

switch (args[0]) {
  case "positions":
    getPosition();
    break;
  case "alch":
    loop(alch, 3);
    break;
  case "tele-alch":
    loop(alchTeleCamelot, 3);
    break;
  case "steal":
    steal();
  default:
    console.log("invalid args");
}
// TODO add as param
// set moveMouse to where the mouse should go
function alch() {
  console.log("time:", new Date());
  robot.moveMouse(1615, 882);
  robot.mouseClick("left", true);
}

function alchTeleCamelot() {
  console.log("time:", new Date());
  robot.moveMouse(1615, 882);
  robot.mouseClick("left", true);
  setTimeout(() => {
    robot.moveMouse(1590, 859);
    robot.mouseClick("left", false);
  }, 800);
}

function steal() {
  const positionStall = [589, 605];

  const positionItem = [1478, 801];

  loop(() => {
    robot.moveMouse(...positionStall);
    console.log("moved mouse");
    robot.mouseClick("left", false);
    console.log("left clicked");
  }, 3);

  loop(() => {
    robot.keyToggle("shift", "down");
    console.log("toggled shift down");
    robot.moveMouse(...positionItem);
    console.log("moved mouse");
    robot.mouseClick("left", false);
    console.log("left clicked");
    robot.keyToggle("shift", "up");
    console.log("toggled shift up");
  }, 4.5);
}

// move the mouse to where I want to know the position
function getPosition() {
  while (true) {
    console.log(robot.getMousePos());
  }
}

// loops on a semi-random interval (fn: function to run, sec: seconds)
function loop(fn, sec) {
  var rand = sec * 1000.0 + (Math.floor(Math.random() * 6) + 1) * Math.random();
  setTimeout(function () {
    fn();
    loop(fn, sec);
  }, rand);
}

// 1615 882
