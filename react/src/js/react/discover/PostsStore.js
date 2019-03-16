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
				$push: response.data.results
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
            const index = this.state.posts.findIndex((post) => post.id === id);
			const posts = update(this.state.posts, {
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

    onGetPost(postId) {
        this.setState({
            fetchingPost: true,
            failedToFetchPost: false,
            currentPost: null,
			currentPostImages: []
        });
        RestUtil.sendGET(`posts/${postId}/`).then((response) => {
			const post = response.data.find((post) => post.contentType.includes("text"));
			const images = response.data.filter((post) => post.contentType.includes("image"));
            this.setState({
                fetchingPost: false,
                currentPost: post,
				currentPostImages: images
            });
        }).catch((err) => {
            this.setState({
                fetchingPost: false,
                failedToFetchPost: true
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
