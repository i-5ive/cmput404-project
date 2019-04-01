import Reflux from "reflux";
import update from "immutability-helper";
import _ from "lodash";

import RestUtil from "../util/RestUtil";
import { POSTS_PAGE_SIZE } from "../constants/PostConstants";

export const PostsActions = Reflux.createActions([
    "createPost",
    "getPosts",
    "deletePost",
    "getPost",
    "addComment",
    "getExternalPosts",
    "clearModalMessage"
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
            creatingComment: false,
            successfullyCreatedComment: false,
            failedToCreateComment: false,
            posts: [],
            currentPost: null,
            fetchingPosts: false,
            failedToFetchPosts: false,
            deletingPost: false,
            failedToDeletePost: false,
            fetchingPost: false,
            nextPage: null,
            currentPostImages: []
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
            failedToCreatePost: false,
            invalidSharedUsernames: null
        });
        RestUtil.sendPOST("posts/", data).then(() => {
            this.setState({
                creatingPost: false,
                successfullyCreatedPost: true
            });
        }).catch((err) => {
            this.setState({
                creatingPost: false,
                failedToCreatePost: true,
                invalidSharedUsernames: _.get(err, "response.data.invalidUsers")
            });
            console.error(err);
        });
    }

    onGetPosts(page = 0) {
        const state = {
            fetchingPosts: true,
            failedToFetchPosts: false
        };
        if (page === 0) {
            state.posts = [];
        }
        this.setState(state);
        RestUtil.sendGET("posts/", {
            page: page,
            size: POSTS_PAGE_SIZE
        }).then((response) => {
            const posts = update(this.state.posts, {
                $push: response.data.posts
            });
            this.setState({
                fetchingPosts: false,
                posts: posts,
                nextPage: response.data.next ? page + 1 : null
            });
        }).catch((err) => {
            this.setState({
                fetchingPosts: false,
                failedToFetchPosts: true,
                nextPage: null
            });
            console.error(err);
        });
    }

    onGetExternalPosts(page = 0) {
        const state = {
            fetchingPosts: true,
            failedToFetchPosts: false
        };
        if (page === 0) {
            state.posts = [];
        }
        this.setState(state);
        RestUtil.sendGET("posts/external/", {
            page: page,
            size: POSTS_PAGE_SIZE
        }).then((response) => {
            const posts = update(this.state.posts, {
                $push: response.data.posts
            });
            this.setState({
                fetchingPosts: false,
                posts: posts,
                nextPage: response.data.next ? page + 1 : null
            });
        }).catch((err) => {
            this.setState({
                fetchingPosts: false,
                failedToFetchPosts: true,
                nextPage: null
            });
            console.error(err);
        });
    }

    onDeletePost(id, postId) {
        this.setState({
            deletingPost: id,
            failedToDeletePost: false
        });
        RestUtil.sendDELETE(`posts/${id}/`).then(() => {
            const index = this.state.posts.findIndex((post) => post.id === id),
			 posts = update(this.state.posts, {
                    $splice: [[index, 1]]
                });
            this.setState({
                posts: posts,
                deletingPost: false,
                failedToDeletePost: false
            });
        }).catch((err) => {
            this.setState({
                deletingPost: false,
                failedToDeletePost: id
            });
            console.error(err);
        });
    }

    onGetPost(postId, isExternal) {
        console.log(postId);
        this.setState({
            fetchingPost: true,
            failedToFetchPost: false,
            currentPost: null,
            currentPostImages: []
        });
        // Depending on if the post is external or internal, do a different fetch
        const promise = isExternal ? RestUtil.sendGET(`posts/external/?postUrl=${postId}`)
            : RestUtil.sendGET(`posts/${postId}/`);
        promise.then((response) => {
            const post = (response.data && response.data.post) || (response.data && response.data.posts[0]) || response.data;
            this.setState({
                fetchingPost: false,
                currentPost: post,
                currentPostImages: response.data.images
            });
        }).catch((err) => {
            this.setState({
                fetchingPost: false,
                failedToFetchPost: true
            });
            console.error(err);
        });
    }

    onAddComment(comment) {
        this.setState({
            creatingComment: true,
            successfullyCreatedComment: false,
            failedToCreateComment: false
        });
        console.log("1", comment.post); //this is undefined?!?!!
        RestUtil.sendPOST(`posts/${comment.post}/comments/`, comment).then(() => {
            this.setState({
                creatingComment: false,
                successfullyCreatedComment: true,
                failedToCreateComment: false
            });
        }).catch((err) => {
            this.setState({
                creatingComment: false,
                successfullyCreatedComment: false,
                failedToCreateComment: true
            });
            console.error(err);
        });
    }

    onClearModalMessage() {
        this.setState({
            failedToCreatePost: false
        });
    }
}

export default {
    PostsStore,
    PostsActions
};
