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
  case "steal":
    steal();
}
// TODO add as param
// set moveMouse to where the mouse should go
function alch() {
  console.log("time:", new Date());
  robot.moveMouse(1615, 882);
  robot.mouseClick("left", true);
}

function steal() {
  const positionStall = [873, 555];

  const positionItem = [1478, 801];

  loop(() => {
    robot.moveMouse(...positionStall);
    robot.mouseClick("left", false);
  }, 3);

  loop(() => {
    robot.keyToggle("shift", "down");
    robot.moveMouse(...positionItem);
    robot.mouseClick("left");
    robot.keyToggle("shift", "up");
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
  fn();
  setTimeout(function () {
    console.log(fn);
    fn();
    loop(fn, sec);
  }, rand);
}

// 1615 882
