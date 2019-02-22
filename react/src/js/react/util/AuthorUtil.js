import { SERVER_URL } from "../constants/ServerConstants";

export const isExternalAuthor = (authorId) => {
    return authorId.split("/author/")[0] !== SERVER_URL;
}, createSummaryQuery = (authorUrl, displayName) => {
    return {
        url: authorUrl,
        id: authorUrl,
        displayName: displayName,
        host: authorUrl.split("/author/")[0]
    };
}, getAuthorUrl = (authorId) => {
    if (authorId.includes("http")) {
        return authorId;
    }
    return `${SERVER_URL}/author/${authorId}`;
};
