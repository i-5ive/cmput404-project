import Reflux from "reflux";
import update from "immutability-helper";

import RestUtil from "../util/RestUtil";

export const PostsActions = Reflux.createActions([
    "createPost",
    "getPosts",
    "deletePost",
    "getPost"
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
            allPosts: [],
            currentPost: [],
            fetchingPosts: false,
            failedToFetchPosts: false,
            deletingPost: true,
            failedToDeletePost: false,
            fetchingPost: false
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
            const posts = update(this.state.allPosts, {
                    $push: response.data.results
                }),
                hash = Object.create(null);

            posts.forEach(function(post) {
                if (hash[post.post_id]) {
                    hash[post.post_id].push(post);
                } else {
                    hash[post.post_id] = [post];
                }
            });
            this.setState({
                fetchingPosts: false,
                posts: hash,
                allPosts: posts,
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
        RestUtil.sendDELETE(`posts/${id}/`).then(() => {
            // From mehulmpt, https://stackoverflow.com/questions/48302118/delete-nested-object-base-on-key-in-react
            const newPosts = Object.assign({}, this.state.posts);
            delete newPosts[postId];
            this.setState({
                posts: newPosts,
                deletingPost: false,
                failedToDeletePost: false
            });
        }).catch((err) => {
            this.setState({
                deletingPost: false,
                failedToDeletePost: true
            });
            console.error(err);
        });
    }

    onGetPost(postId) {
        this.setState({
            fetchingPost: true,
            failedToFetchPost: false,
            currentPost: []
        });
        RestUtil.sendGET(`posts/${postId}/`).then((response) => {
            const post = update(this.state.currentPost, {
                $set: response.data
            });

            this.setState({
                fetchingPost: false,
                currentPost: post
            });
        }).catch((err) => {
            this.setState({
                fetchingPost: false,
                failedToFetchPost: true
            });
            console.error(err);
        });
    }
}

export default {
    PostsStore,
    PostsActions
};
