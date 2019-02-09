import rp from "request-promise";

import { SERVER_URL } from "../constants/ServerConstants";

export default class RestUtil {
    /**
     * Sends a POST request to the server
     * @param {String} path - the path to make the request to
     * @param {Object} body - the request body
     * @return {Promise} - a promise that resolves when the request is finished
     */
    static sendPOST(path, body) {
        const options = {
            uri: `${SERVER_URL}/${path}`,
            headers: {
                "Content-Type": "application/json"
            },
            json: true,
            body: body
        };
        return rp.post(options);
    }

    /**
     * Sends a GET request to the server
     * @param {String} path - the path to make the request to
     * @return {Promise} - a promise that resolves when the request is finished
     */
    static sendGET(path) {
        const options = {
            uri: `${SERVER_URL}/${path}`,
            json: true
        };
        return rp.get(options);
    }
}
