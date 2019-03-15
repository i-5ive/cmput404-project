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
            isLoadingPosts: false
        };
        this.listenables = Actions;

        if (process.env.NODE_ENV === "development") {
            window.DEV_HOME_STORE = this;
        }
    }

    onLoadPosts(page) {
        this.setState({
            isLoadingPosts: true,
            errorLoadingPosts: false
        });

        RestUtil.sendGET(`author/posts/`, {
            page: page
        }).then((res) => {
            const posts = update(this.state.posts, {
                $push: res.posts
            });
            this.setState({
                posts: posts,
                isLoadingPosts: false
            });
        }).catch((err) => {
            this.setState({
                isLoadingPosts: false,
                errorLoadingPosts: true
            });
            console.error(err);
        });
    }
}
