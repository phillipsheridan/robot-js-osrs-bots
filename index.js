/* 

TODO

- add TS support
- make inputs passable from command line or let the use click where they want instead of finding own positions
- setup only works on RL, my monitor, with my postitions. you will need to update the hard coded values - 
- make the magic numbers consts

*/

var robot = require("robotjs");

const ALCH_TIMEOUT = 3;
const TELE_ALCH_TIMEOUT = 3.2;
const POSITION_STALL = [589, 605];
const POSITION_ITEMS = [1478, 801];
const ALCH_POSITION = [1615, 882];
const STOP_POSITION = [1159, 470];
const STOP_PIXEL_COLOR = "03e9a9";

// todo use args

const args = process.argv.slice(2);

switch (args[0]) {
  case "positions":
    scan();
    break;
  case "alch":
    loop(alch, ALCH_TIMEOUT);
    break;
  case "tele-alch":
    loop(alchTeleCamelot, TELE_ALCH_TIMEOUT);
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
  robot.moveMouse(...ALCH_POSITION);
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
  loop(() => {
    robot.moveMouse(...POSITION_STALL);
    console.log("moved mouse");
    robot.mouseClick("left", false);
    console.log("left clicked");
  }, 3);

  loop(() => {
    robot.keyToggle("shift", "down");
    console.log("toggled shift down");
    robot.moveMouse(...POSITION_ITEMS);
    console.log("moved mouse");
    robot.mouseClick("left", false);
    console.log("left clicked");
    robot.keyToggle("shift", "up");
    console.log("toggled shift up");
  }, 4.5);
}

// move the mouse to where I want to know the position/color
function scan() {
  while (true) {
    checkForStopCondition();
    const position = robot.getMousePos();
    const { x, y } = position;
    console.log(robot.getMousePos());
    console.log(robot.getPixelColor(x, y));
  }
}

// loops on a semi-random interval (fn: function to run, sec: seconds)
function loop(fn, sec) {
  var rand = sec * 1000.0 + (Math.floor(Math.random() * 6) + 1) * Math.random();
  setTimeout(function () {
    fn();
    checkForStopCondition();
    loop(fn, sec);
  }, rand);
}

function checkForStopCondition() {
  console.log(STOP_PIXEL_COLOR);
  console.log(STOP_POSITION);
  const stopPixelColor = robot.getPixelColor(
    STOP_POSITION[0],
    STOP_POSITION[1]
  );
  console.log("MUSIC BUTTON COLOR:", stopPixelColor);
  // halt condition
  if (stopPixelColor === STOP_PIXEL_COLOR) {
    process.exit();
  }
}
