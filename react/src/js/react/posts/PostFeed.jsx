import React from "react";

import Post from "./Post";

/**
 * This is componenet will GET from the posts database to get all the posts.
 * From here it will dynamically create components for all the posts
 */
export default class PostFeed extends React.Component {
    constructor(props) {
        super(props);
        this.getPosts = this.getPosts.bind(this);
        this.state = {
            posts: [],
            promiseDone: false
        };
    }

    componentDidMount() {
        this.getPosts();
    }

    /**
     * GET's to the database
     */
    getPosts() {
        // TODO: actually connect this to the database
        // TODO: currently this will only work locally, perhaps we have to fix that?

        // fetch("http://localhost:8000/api/posts")
        //   .then(res => res.json())
        //   .then(text => {
        //       this.setState({posts: text});
        //       this.setState({promiseDone: true});
        //   });

        // TODO: remove the 2 lines below. It is fake data so Mandy can make the UI
        // TODO: get the post id from the json object and pass it to the post object
        this.setState({ posts: ["thing", "thing2"] });
        this.setState({ promiseDone: true });
    }

    render() {
        // TODO: if we want to be good we could return a loading screen instead of null
        if (!this.state.promiseDone) { return null; }
        return (
            <div className="post-feed">
                {this.state.posts.map(post => (
                    <Post className="post" key={post} postId={post} />
                ))}
            </div>
        );
    }
}
