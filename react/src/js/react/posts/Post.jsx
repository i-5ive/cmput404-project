import React from "react";
import Reflux from "reflux";
import PropTypes from "prop-types";

import { Button } from "react-bootstrap";
import { PostsStore, PostsActions } from "./PostsStore";
import AuthStore from "../auth/AuthStore";
import { Thumbnail } from "react-bootstrap";

import { formatDate } from "../util/DateUtil";

/**
 * Displays a singular post
 */
export default class Post extends Reflux.Component {
    static propTypes = {
        className: PropTypes.string.isRequired,
        post: PropTypes.object.isRequired
    }

    constructor(props) {
        super(props);
        this.stores = [PostsStore, AuthStore];
    }

    renderContent = () => {
        const type = this.props.post.contentType,
            content = this.props.post.content;
        if (type === ("image/png;base64" || "image/jpeg;base64")) {
            const name = `data:${type},${content}`;
            return <img src={name} />;
        } else {
            return <p className="content">{content}</p>;
        }
    }

    // TODO
    renderComments() {
        return null;
    }

    handleDeletePost = () => {
        PostsActions.deletePost(this.props.post.id, this.props.post.post_id);
    }

    render() {
        const { post } = this.props;
        console.log(post);
        return (
            <Thumbnail>
                <div className="post-header">
                    <i className="fas fa-user-lock">{post.visibility}</i>
                    <Button
                        variant="primary"
                        className="delete-button"
                        onClick={this.handleDeletePost}>
                        <i className="far fa-trash-alt" />
                    </Button>
                </div>
                <h4 className="post-title">
                    {
                        post.title
                    }
                </h4>
                <p>
                    {
                        formatDate(post.published)
                    }
                </p>
                <p className="post-body">
                    {
                        this.renderContent()
                    }
                </p>
                <p className="categories">{post.categories}</p>
                <p className="source">{post.source}</p>
                <p className="origin">{post.origin}</p>
                {
                    this.renderComments()
                }
            </Thumbnail>
        );
    }
}
