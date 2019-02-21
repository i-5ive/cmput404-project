import React from "react";
import Reflux from "reflux";

import ProfileStore from "./ProfileStore";
import LoadingComponent from "../misc/LoadingComponent";

export default class ProfileGithubStream extends Reflux.Component {
    constructor(props) {
        super(props);
        this.store = ProfileStore;
        this.state = {
            mountedGithub: false
        };
    }

    shouldComponentUpdate(prevProps, prevState) {
        return this.state.profileDetails !== prevState.profileDetails || this.state.mountedGithub !== prevState.mountedGithub;
    }

    componentDidUpdate() {
        if (!this.state.mountedGithub && this.state.profileDetails && this.state.profileDetails.github && document.querySelector("#feed")) {
            GitHubActivity.feed({
                username: this.state.profileDetails.github.split(".com/")[1],
                selector: "#feed"
            });
            this.setState({
                mountedGithub: true
            });
        }
    }

    render() {
        if (!this.state.profileDetails) {
            return <LoadingComponent />;
        } else if (!this.state.profileDetails.github) {
            return <div>This user has not enabled github integration.</div>;
        }
        return <div id="feed" />
    }
}