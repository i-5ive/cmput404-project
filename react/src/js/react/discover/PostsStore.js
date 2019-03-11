import Reflux from "reflux";
import update from "immutability-helper";

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
        RestUtil.sendPOST("posts/", data).then(() => {
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

    onGetPosts(page) {
        this.setState({
            fetchingPosts: true,
            failedToFetchPosts: false
        });
        RestUtil.sendGET("posts/", {
            page: page
        }).then((response) => {
            const posts = update(this.state.posts, {
                $push: response.data.results
            });
            this.setState({
                fetchingPosts: false,
                posts: posts,
                currentPageNumber: page
            });
        }).catch((err) => {
            this.setState({
                fetchingPosts: false,
                failedToFetchPosts: true
            });
            console.error(err);
        });
    }

    onDeletePost(id, postId) {
        this.setState({
            deletingPost: true,
            failedToDeletePost: false
        });
        RestUtil.sendDELETE(`posts/${id}`).then(() => {
            // From pscl, https://stackoverflow.com/questions/29527385/removing-element-from-array-in-component-state
            this.setState((prevState) => ({
                posts: prevState.posts.filter((post) => post.post_id !== postId),
                deletingPost: false,
                failedToDeletePost: false
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
