// Python just works better for this stuff


// import robot from '@jitsi/robotjs';

// const ALCH_TIMEOUT = 3;
// const TELE_ALCH_TIMEOUT = 3.2;
// const POSITION_STALL: [number, number] = [589, 605];
// const POSITION_ITEMS: [number, number] = [1478, 801];
// const ALCH_POSITION: [number, number] = [1615, 882];
// const STOP_POSITION: [number, number] = [1159, 470];
// const STOP_PIXEL_COLOR = "03e9a9";

// const args = process.argv.slice(2);

// switch (args[0]) {
//     case "positions":
//         scan();
//         break;
//     case "alch":
//         loop(alch, ALCH_TIMEOUT);
//         break;
//     case "tele-alch":
//         loop(alchTeleCamelot, TELE_ALCH_TIMEOUT);
//         break;
//     case "steal":
//         steal();
//         break;
//     default:
//         console.log("invalid args");
// }

// function alch() {
//     console.log("time:", new Date());
//     robot.moveMouse(...ALCH_POSITION);
//     robot.mouseClick("left", true);
// }

// function alchTeleCamelot() {
//     console.log("time:", new Date());
//     robot.moveMouse(1615, 882);
//     robot.mouseClick("left", true);
//     setTimeout(() => {
//         robot.moveMouse(1590, 859);
//         robot.mouseClick("left", false);
//     }, 800);
// }

// function steal() {
//     loop(() => {
//         robot.moveMouse(...POSITION_STALL);
//         console.log("moved mouse");
//         robot.mouseClick("left", false);
//         console.log("left clicked");
//     }, 3);

//     loop(() => {
//         robot.keyToggle("shift", "down");
//         console.log("toggled shift down");
//         robot.moveMouse(...POSITION_ITEMS);
//         console.log("moved mouse");
//         robot.mouseClick("left", false);
//         console.log("left clicked");
//         robot.keyToggle("shift", "up");
//         console.log("toggled shift up");
//     }, 4.5);
// }

// import fs from "fs";
// import path from "path";

// function scan() {
//     setInterval(() => {
//         // Take screenshot at the beginning of each interval
//         const screen = robot.screen.capture(0, 0, robot.getScreenSize().width, robot.getScreenSize().height);
//         const image = Buffer.from(screen.image);
//         const timestamp = Date.now();
//         const screenshotPath = path.join("input-images", `screenshot_${timestamp}.png`);
//         fs.writeFileSync(screenshotPath, image);

//         checkForStopCondition();
//         const position = robot.getMousePos();
//         const { x, y } = position;
//         console.log(robot.getMousePos());
//         console.log(robot.getPixelColor(x, y));
//     }, 200);
// }

// function loop(fn: () => void, sec: number) {
//     const rand = sec * 1000.0 + (Math.floor(Math.random() * 6) + 1) * Math.random();
//     setTimeout(function () {
//         fn();
//         checkForStopCondition();
//         loop(fn, sec);
//     }, rand);
// }

// function checkForStopCondition() {
//     console.log(STOP_PIXEL_COLOR);
//     console.log(STOP_POSITION);
//     const stopPixelColor = robot.getPixelColor(
//         STOP_POSITION[0],
//         STOP_POSITION[1]
//     );
//     console.log("MUSIC BUTTON COLOR:", stopPixelColor);
//     if (stopPixelColor === STOP_PIXEL_COLOR) {
//         process.exit();
//     }
// }
