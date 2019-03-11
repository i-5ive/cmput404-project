import React from "react";
import Reflux from "reflux";
import PropTypes from "prop-types";

import { PostsStore, PostsActions } from "../discover/PostsStore";
import { Thumbnail, Button } from "react-bootstrap";

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
        this.store = PostsStore;
    }

    // TODO Need to render properly
    // From VinayC, https://stackoverflow.com/questions/8499633/how-to-display-base64-images-in-html
    renderContent = () => {
        const { contentType, content } = this.props.post;
        if (contentType === ("image/png;base64" || "image/jpeg;base64")) {
            const name = `data:${contentType},${content}`;
            return <img src={name} />;
        } else {
            return <p className="content">{content}</p>;
        }
    }

    // TODO
    renderComments() {
        return null;
    }

    renderFooter() {
        const { post } = this.props;
        return (
            <div className="post-footer">
                <p className="categories">{post.categories}</p>
                { post.source ? <a href={post.source} className="source">source</a> : null}
                { post.origin ? <a href={post.origin}>origin</a> : null }
            </div>
        );
    }

    handleDeletePost = () => {
        PostsActions.onDeletePost(this.props.post.id, this.props.post.post_id);
    }

    render() {
        const { post } = this.props;
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
                {this.renderFooter()}
                {
                    this.renderComments()
                }
            </Thumbnail>
        );
    }
}
