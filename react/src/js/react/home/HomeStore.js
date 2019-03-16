import Reflux from "reflux";
import update from "immutability-helper";

import Actions from "./HomeActions";

import RestUtil from "../util/RestUtil";

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

    onLoadPosts(page=0) {
		const state = {
            isLoadingPosts: true,
            errorLoadingPosts: false
        };
		if (page === 0) {
			state.posts = [];
		}
        this.setState(state);

        RestUtil.sendGET("posts/feed/", {
            page: page
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
}
