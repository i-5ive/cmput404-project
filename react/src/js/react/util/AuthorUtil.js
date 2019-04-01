import { HOST_URL } from "../constants/ServerConstants";

export const
    /**
     * Determines whether the specified author is external or not
     * @param {String} authorId - the URL or ID of the author
     * @return {boolean} - whether the author is external or not
     */
    isExternalAuthor = (authorId) => {
        return authorId.includes("/author/") && authorId.split("/author/")[0] !== HOST_URL;
    },
    /**
     * Creates a summary query used to represent an author
     * @param {String} authorUrl - the unique URL of the author
     * @param {String} displayName - the display name of the author
     * @return {Object} - the summary query representing the author
     */
    createSummaryQuery = (authorUrl, displayName) => {
        return {
            url: authorUrl,
            id: authorUrl,
            displayName: displayName,
            host: authorUrl.split("/author/")[0]
        };
    },
    /**
     * Gets the unique URL representing an author
     * @param {String} authorId - the unique ID of the author (can be a URL)
     * @return {String} - the unique URL representing the author
     */
    getAuthorUrl = (authorId) => {
        if (authorId.includes("http")) {
            return authorId;
        }
        return `${HOST_URL}/author/${authorId}`;
    },
    /**
     * Gets the unique ID of an author
     * @param {String} authorId - the unique URL or ID of the author
     * @return {String} - the input URL if the author is external, or their uuid otherwise
     */
    getAuthorId = (authorId) => {
        if (isExternalAuthor(authorId)) {
            return authorId;
        }
        return authorId.includes("/author/") ? authorId.split("/author/")[1] : authorId;
    },
    /**
     * Escapes the URL to make it compatible with our server
     * @param {String} url - the url to escape
     * @return {String} - an escaped version of the URL
     */
    escapeUrl = (url) => {
        return window.btoa(url);
    };
