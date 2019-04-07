import Reflux from "reflux";
import update from "immutability-helper";
import _ from "lodash";

import RestUtil from "../util/RestUtil";
import { POSTS_PAGE_SIZE } from "../constants/PostConstants";
import { HOST_URL } from "../constants/ServerConstants";

export const PostsActions = Reflux.createActions([
    "createPost",
    "getPosts",
    "deletePost",
    "editPost",
    "getPost",
    "putPost",
    "addComment",
    "getExternalPosts",
    "clearModalMessage",
    "loadComments",
    "clearEditNotifications"
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
            currentPostImages: [],
            comments: []
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

    onEditPost(id, postId) {
        window.location.href = `post/${id}/edit`;
    }

    onPutPost(data) {
        this.setState({
            isEditingPost: true,
            errorEditingPost: false,
            successfullyEditedPost: false
        });
        data.author = this.state.currentPost.author;
        const id = window.location.href.endsWith("edit") && window.location.href.split("/post/")[1].split("/edit")[0];
        RestUtil.sendPOST(`posts/${id}/update/`, data).then(() => {
            this.setState({
                isEditingPost: false,
                successfullyEditedPost: true
            });
        }).catch((err) => {
            this.setState({
                isEditingPost: false,
                errorEditingPost: true
            });
            console.error(err);
        });
    }

    onClearEditNotifications() {
        this.setState({
            errorEditingPost: false,
            successfullyEditedPost: false
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
                currentPost: post
            });
            if (post.images) {
                Promise.all(post.images.map((img) => {
                    return RestUtil.sendGET(img.split(".com/")[1] || img.split(":8000/")[1]);
                })).then((allImgs) => {
                    this.setState({
                        currentPostImages: allImgs.map((res) => `data:${res.data}`)
                    });
                });
            }
        }).catch((err) => {
            this.setState({
                fetchingPost: false,
                failedToFetchPost: true
            });
            console.error(err);
        });
    }

    onAddComment(id, comment, origin) {
        this.setState({
            creatingComment: true,
            successfullyCreatedComment: false,
            failedToCreateComment: false
        });
        const external = origin.split("/posts/")[0] !== HOST_URL,
            promise = external ? (
                RestUtil.sendPOST("posts/createExternalComment/", {
                    postUrl: origin,
                    comment: comment
                })
            ) : RestUtil.sendPOST(`posts/${id}/comments/`, {
                comment: comment,
                query: "addComment"
            });
        promise.then(() => {
            const state = {
                creatingComment: false,
                successfullyCreatedComment: true,
                failedToCreateComment: false
            };
            if (external && this.state.currentPost) {
                const post = update(this.state.currentPost, {
                    comments: {
                        $unshift: [comment]
                    }
                });
                state.currentPost = post;
            }
            this.setState(state);
            if (!external && this.state.currentPost) {
                this.onLoadComments(this.state.currentPost);
            }
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

    onLoadComments(post, page = 0) {
        const state = {
                fetchingComments: true,
                failedToFetchComments: false
            },
		 isExternal = post.origin.split("/posts/")[0] !== HOST_URL;
        if (isExternal) {
            state.comments = post.comments || [];
            state.fetchingComments = false;
        } else if (page === 0) {
            state.comments = [];
        }

        this.setState(state);
        if (isExternal) {
            return;
        }
        RestUtil.sendGET(`posts/${post.id}/comments/`, {
            page: page,
            size: POSTS_PAGE_SIZE
        }).then((response) => {
            const comments = update(this.state.comments, {
                $push: response.data.comments
            });
            this.setState({
                fetchingComments: false,
                comments: comments,
                nextCommentsPage: response.data.next ? page + 1 : null
            });
        }).catch((err) => {
            this.setState({
                fetchingComments: false,
                failedToFetchComments: true,
                nextCommentsPage: null
            });
            console.error(err);
        });
    }
}

export default {
    PostsStore,
    PostsActions
};
