var robot = require("robotjs");

// while (true) {
//   const rand = (Math.floor(Math.random() * 6) + 1) * 0.1 + Math.random();
//   console.log(rand);
//   setTimeout(() => {
//     // robot.moveMouse(1615, 882);
//     // robot.mouseClick("left", true);
//     console.log("move to place and click");
//   }, 3000.0 + rand);
// }

function doSomething() {
  console.log("time:", new Date());
  robot.moveMouse(1615, 882);
  robot.mouseClick("left", true);
}

(function loop() {
  var rand = 3000.0 + (Math.floor(Math.random() * 6) + 1) * Math.random();
  setTimeout(function () {
    doSomething();
    loop();
  }, rand);
})();

// 1615 882
