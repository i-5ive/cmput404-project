export default class CookieUtil {
  static deleteCookie(name) {
    // Credit to emii at https://stackoverflow.com/a/23995984
    document.cookie = `${name}=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;`;
  }
}
