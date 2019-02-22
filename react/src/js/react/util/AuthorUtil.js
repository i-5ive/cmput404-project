import { SERVER_URL } from "../constants/ServerConstants";

export const
    /**
     * Determines whether the specified author is external or not
     * @param {String} authorUrl - the URL of the author
     * @return {boolean} - whether the author is external or not
     */
    isExternalAuthor = (authorUrl) => {
        return authorUrl.split("/author/")[0] !== SERVER_URL;
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
        return `${SERVER_URL}/author/${authorId}`;
    };
