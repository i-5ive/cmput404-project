import { SERVER_URL } from "../constants/ServerConstants";

export const isExternalAuthor = (authorId) => {
    return authorId.split("/author/")[0] !== SERVER_URL;
};
