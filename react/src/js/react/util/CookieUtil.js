import cookie from "cookie";

export default class CookieUtil {
    static deleteCookie(name) {
    // Credit to emii at https://stackoverflow.com/a/23995984
        document.cookie = `${name}=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;`;
    }

    static getValue(name) {
        return cookie.parse(document.cookie)[name];
    }

    static setCookie(name, value) {
        document.cookie = `${name}=${value}; max-age=86400`;
    }
}
