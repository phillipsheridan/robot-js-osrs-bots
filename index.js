var robot = require("robotjs");

// todo use args

// const myArgs = process.argv.slice(2);
// console.log('myArgs: ', myArgs);

// TODO add as param
// set moveMouse to where the mouse should go
function alch_clicks() {
  console.log("time:", new Date());
  robot.moveMouse(1615, 882);
  robot.mouseClick("left", true);
}

(function loop() {
  var rand = 3000.0 + (Math.floor(Math.random() * 6) + 1) * Math.random();
  setTimeout(function () {
    alch_clicks();
    loop();
  }, rand);
})();

// 1615 882
