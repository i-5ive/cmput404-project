import axios from "axios";

import { SERVER_URL } from "../constants/ServerConstants";

// Credit to krescruz at https://stackoverflow.com/a/48118202 for this
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";

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
     * @param {Object?} query - an optional object representing the query string
     * @param {boolean?} externalHost - whether the request is being made to an external server or not
     * @return {Promise} - a promise that resolves when the request is finished
     */
    static sendGET(path, query = {}, externalHost = false) {
        const uri = externalHost ? path : `${SERVER_URL}/${path}`;
        return axios(uri, {
            params: query,
            withCredentials: !externalHost
        });
    }

    /**
     * Sends a DELETE request to the server
     * @param {String} path - the path to make the request to (ex: posts/<id>)
     * @return {Promise} - a promise that resolves when the request is finished
     */
    static sendDELETE(path) {
        const options = {
            withCredentials: true,
            method: "delete",
            url: `${SERVER_URL}/${path}`
        };
        return axios(options);
    }
}
