import React from "react";

import PostFeed from "./PostFeed";
import NewPostButton from "./NewPostButton";

export default class PostPage extends React.Component {
    render() {
        return (
            <div>
                <PostFeed/>
                <NewPostButton/>
            </div>
        );
    }
}
