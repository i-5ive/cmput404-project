import axios from "axios";

import { SERVER_URL } from "../constants/ServerConstants";

export default class RestUtil {
    /**
     * Sends a POST request to the server
     * @param {String} path - the path to make the request to (ex: login/)
     * @param {Object} body - the request body
     * @return {Promise} - a promise that resolves when the request is finished
     */
    static sendPOST(path, body) {
        const options = {
            data: body,
            withCredentials: true,
            method: "post",
            url: `${SERVER_URL}/${path}`
        };
        return axios(options);
    }

    /**
     * Sends a GET request to the server
     * @param {String} path - the path to make the request to (ex: authors/)
     * @return {Promise} - a promise that resolves when the request is finished
     */
    static sendGET(path) {
        return axios.get(`${SERVER_URL}/${path}`);
    }
}
