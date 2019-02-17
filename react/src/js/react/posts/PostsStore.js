import Reflux from "reflux";

import RestUtil from "../util/RestUtil";

export const PostsActions = Reflux.createActions([
    "createPost"
]);

// TODO delete posts?, getposts

const makeUserQueryObject = (user) => {
    return {
        id: user.id,
        host: user.host,
        displayName: user.displayName,
        url: user.url
    };
};

/**
 * This store keeps track of the state of components that deal with creating posts
 */
export class PostsStore extends Reflux.Store {
    constructor() {
        super();
        this.state = {
            errorLoadingRequests: false,
            creatingPost: false,
            successfullyCreatedPost: false,
            failedToCreatePost: false
        };
        this.listenables = PostsActions;

        if (process.env.NODE_ENV === "development") {
            window.DEV_POSTS_STORE = this;
        }
    }

    onCreatePost(user) {
        this.setState({
            creatingPost: true,
            successfullyCreatedPost: false,
            failedToCreatePost: false
        });

        RestUtil.sendPOST("posts/", {
            query: "createpost",
            author: makeUserQueryObject(user)
        }).then(() => {
            this.setState({
                creatingPost: false,
                successfullyCreatedPost: true,
                failedToCreatePost: false
            });
        }).catch((err) => {
            this.setState({
                creatingPost: false,
                successfullyCreatedPost: false,
                failedToCreatePost: true
            });
            console.error(err);
        });
    }
}

export default {
    PostsStore,
    PostsActions
};
