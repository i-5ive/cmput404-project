import Reflux from "reflux";

import RestUtil from "../util/RestUtil";

export const PostsActions = Reflux.createActions([
    "createPost",
    "getPosts",
    "deletePost"
]);

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
            failedToCreatePost: false,
            posts: [],
            fetchingPosts: false,
            failedToFetchPosts: false,
            deletingPost: true,
            failedToDeletePost: false
        };
        this.listenables = PostsActions;

        if (process.env.NODE_ENV === "development") {
            window.DEV_POSTS_STORE = this;
        }
    }

    onCreatePost(data) {
        this.setState({
            creatingPost: true,
            successfullyCreatedPost: false,
            failedToCreatePost: false
        });

        RestUtil.sendPOST("posts/", {
            query: "createpost",
            postData: JSON.stringify(data)
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

    getPosts() {
        this.setState({
            fetchingPosts: true,
            failedToFetchPosts: false
        });
        RestUtil.sendGET("posts/").then((response) => {
            console.log(response);
            this.setState({
                fetchingPosts: false,
                posts: response.data.results
            });
        }).catch((err) => {
            this.setState({
                fetchingPosts: false,
                failedToFetchPosts: true
            });
            console.error(err);
        });
    }

    deletePost(id, postId) {
        this.setState({
            deletingPost: true,
            failedToDeletePost: false
        });
        RestUtil.sendDELETE(`posts/${id}`).then(() => {
            this.setState({
                deletingPost: false,
                failedToDeletePost: false
            });
            // From pscl, https://stackoverflow.com/questions/29527385/removing-element-from-array-in-component-state
            this.setState((prevState) => ({
                posts: prevState.posts.filter((post) => post.post_id !== postId)
            }));
        }).catch((err) => {
            this.setState({
                fetchingPosts: false,
                failedToDeletePost: true
            });
            console.error(err);
        });
    }
}

export default {
    PostsStore,
    PostsActions
};
