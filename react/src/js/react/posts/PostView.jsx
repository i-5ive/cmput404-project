import React from "react";
import Reflux from "reflux";

import { Alert, Button, Form, FormGroup, FormControl, Thumbnail } from "react-bootstrap";
import ReactMarkdown from "react-markdown";

import { PostsStore, PostsActions } from "../discover/PostsStore";
import LoadingComponent from "../misc/LoadingComponent";
import { formatDate } from "../util/DateUtil";
import Post from "./Post";
import AuthStore from "../auth/AuthStore";
import { Link } from "react-router-dom";

/**
 * Renders details about one specific post
 */
export default class PostView extends Reflux.Component {
    constructor(props) {
        super(props);
        this.stores = [PostsStore, AuthStore];
    }

    componentDidMount() {
        PostsActions.getPost(this.props.match.params.id);
    }

    handleCommentSubmit = (e) => {
        e.preventDefault();
        if (e.currentTarget.elements.comment.value !== "") {
            // eslint-disable-next-line no-undef
            const formData = new FormData(),
                form = e.currentTarget,
                data = {
                    comment: form.elements.comment.value,
                    author: this.state.userId,
                    contentType: form.elements.contentType.value,
                    post: this.state.currentPost.id
                };
            formData.append("commentData", JSON.stringify(data));
            formData.append("query", "addComment");
            console.log("data", data);
            console.log("form data", formData);
            console.log(this.state.currentPost);
            PostsActions.addComment(data);
        }
    }

    renderCommentText(comment) {
        if (comment.contentType === "text/markdown") {
            return <ReactMarkdown source={comment.comment} />;
        } else {
            return <span>{comment.comment}</span>;
        }
    }

    renderComments() {
        console.log("comments", this.state.currentPost.comments);
        const comments = this.state.currentPost.comments.map((comment) => (
            <Thumbnail key={comment.id}>
                <div className="comment">
                    {this.renderCommentText(comment)} <br/>
                    Posted by <Link to={`/profile/${encodeURIComponent(comment.author.url)}/`}>{comment.author.displayName}</Link>  on {formatDate(comment.published)}
                </div>
            </Thumbnail>

        ));
        return comments;
    }

    renderMakeComments() {
        return (
            <Form onSubmit={this.handleCommentSubmit}>
                <FormGroup controlId="comment">
                    <FormControl bsSize="sm" name="comment" type="text" placeholder="Comment here..." />
                </FormGroup>
                <FormGroup controlId="contentType">
                    <FormControl name="contentType" className="comments-content-type" componentClass="select">
                        <option value="text/plain">Plaintext</option>
                        <option value="text/markdown">Markdown</option>
                    </FormControl>
                    <Button bsStyle="primary" className="submit-button submit-button-comment" type="submit">
                        Comment
                    </Button>
                </FormGroup>
            </Form>
        );
    }

    render() {
        if (this.state.failedToFetchPost) {
            return <Alert bsStyle="danger">An error occurred while fetching the post</Alert>;
        } else if (!this.state.currentPost) {
            return <LoadingComponent />;
        }
        return (
            <div className="postView">
                <Post
                    post={this.state.currentPost}
                    images={this.state.currentPostImages}
                    isPostView />
                <hr className="comment-hr"/>
                {
                    this.renderComments()
                }
                {this.renderMakeComments()}
            </div>
        );
    }
}
