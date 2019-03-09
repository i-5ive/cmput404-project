import Reflux from "reflux";

const Actions = Reflux.createActions([
  "handleLogin",
  "parseLoginCookies",
  "handleRegistration",
  "resetRegistrationNotifications",
  "resetLoginNotifications",
  "handleLogout"
]);

export default Actions;
