import React from "react";

import PostFeed from "./PostFeed";

export default class PostPage extends React.Component {
    render() {
        return (
            <div>
                <div className="filter-posts-wrapper">
                    <p className="filter-posts-text">
                        I want to see:
                    </p>
                    <input type="checkbox" name="Friends" value="Friends"/>
                    <label htmlFor="Friends">Friends</label>
                    <input type="checkbox" name="FOAF" value="FOAF"/>
                    <label htmlFor="FOAF">FOAF</label>
                    <input type="checkbox" name="Public" value="Public"/>
                    <label htmlFor="Public">Public</label>
                </div>
                <PostFeed/>
            </div>
        );
    }
}
