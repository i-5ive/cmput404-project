import Reflux from "reflux";
import update from "immutability-helper";

import Actions from "./HomeActions";

import RestUtil from "../util/RestUtil";
import { POSTS_PAGE_SIZE } from "../constants/PostConstants";

/**
 * This store keeps track of the state of components that deal with posts on the home page of the app
 */
export default class HomeStore extends Reflux.Store {
    constructor() {
        super();
        this.state = {
            posts: [],
            isLoadingPosts: false,
            nextPage: null
        };
        this.listenables = Actions;

        if (process.env.NODE_ENV === "development") {
            window.DEV_HOME_STORE = this;
        }
    }

    onLoadPosts(page = 0) {
        const state = {
            isLoadingPosts: true,
            errorLoadingPosts: false
        };
        if (page === 0) {
            state.posts = [];
        }
        this.setState(state);

        RestUtil.sendGET("posts/feed/", {
            page: page,
            size: POSTS_PAGE_SIZE
        }).then((res) => {
            const posts = update(this.state.posts, {
                $push: res.data.posts
            });
            this.setState({
                posts: posts,
                isLoadingPosts: false,
                nextPage: res.data.next ? page + 1 : null
            });
        }).catch((err) => {
            this.setState({
                isLoadingPosts: false,
                errorLoadingPosts: true,
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

    onReloadPosts() {
        this.setState({
            posts: []
        });
        this.onLoadPosts();
    }
}
