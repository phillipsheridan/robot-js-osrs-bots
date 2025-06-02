"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const robotjs_1 = __importDefault(require("@jitsi/robotjs"));
const ALCH_TIMEOUT = 3;
const TELE_ALCH_TIMEOUT = 3.2;
const POSITION_STALL = [589, 605];
const POSITION_ITEMS = [1478, 801];
const ALCH_POSITION = [1615, 882];
const STOP_POSITION = [1159, 470];
const STOP_PIXEL_COLOR = "03e9a9";
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
        break;
    default:
        console.log("invalid args");
}
function alch() {
    console.log("time:", new Date());
    robotjs_1.default.moveMouse(...ALCH_POSITION);
    robotjs_1.default.mouseClick("left", true);
}
function alchTeleCamelot() {
    console.log("time:", new Date());
    robotjs_1.default.moveMouse(1615, 882);
    robotjs_1.default.mouseClick("left", true);
    setTimeout(() => {
        robotjs_1.default.moveMouse(1590, 859);
        robotjs_1.default.mouseClick("left", false);
    }, 800);
}
function steal() {
    loop(() => {
        robotjs_1.default.moveMouse(...POSITION_STALL);
        console.log("moved mouse");
        robotjs_1.default.mouseClick("left", false);
        console.log("left clicked");
    }, 3);
    loop(() => {
        robotjs_1.default.keyToggle("shift", "down");
        console.log("toggled shift down");
        robotjs_1.default.moveMouse(...POSITION_ITEMS);
        console.log("moved mouse");
        robotjs_1.default.mouseClick("left", false);
        console.log("left clicked");
        robotjs_1.default.keyToggle("shift", "up");
        console.log("toggled shift up");
    }, 4.5);
}
function scan() {
    setInterval(() => {
        checkForStopCondition();
        const position = robotjs_1.default.getMousePos();
        const { x, y } = position;
        console.log(robotjs_1.default.getMousePos());
        console.log(robotjs_1.default.getPixelColor(x, y));
    }, 200);
}
function loop(fn, sec) {
    const rand = sec * 1000.0 + (Math.floor(Math.random() * 6) + 1) * Math.random();
    setTimeout(function () {
        fn();
        checkForStopCondition();
        loop(fn, sec);
    }, rand);
}
function checkForStopCondition() {
    console.log(STOP_PIXEL_COLOR);
    console.log(STOP_POSITION);
    const stopPixelColor = robotjs_1.default.getPixelColor(STOP_POSITION[0], STOP_POSITION[1]);
    console.log("MUSIC BUTTON COLOR:", stopPixelColor);
    if (stopPixelColor === STOP_PIXEL_COLOR) {
        process.exit();
    }
}
