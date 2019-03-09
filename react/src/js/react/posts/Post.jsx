import React from "react";
import PropTypes from "prop-types";

import { Thumbnail } from "react-bootstrap";

import { formatDate } from "../util/DateUtil";

/**
 * Displays a singular post
 */
export default class Post extends React.Component {
    static propTypes = {
        post: PropTypes.object.isrequired
    }

    // TODO
    renderComments() {
        return null;

        /* <div className="comment-wrapper">
			{this.state.comments.map(comment => (
				<p className="comment" key={comment}>comment</p>
			))}
			<div className="comment-feild">
				<textarea className="comment-input" id={this.props.postId} name="text" rows="1" wrap="soft" />
				<button className="send-comment-button" onClick={this.makeComment}>
					<i className="fa fa-paper-plane send-comment-button" />
				</button>
			</div>
		</div> */
    }

    render() {
        return (
            <Thumbnail>
                <h4 className="post-title">
                    {
                        this.props.post.title
                    }
                </h4>
                <p>
                    {
                        formatDate(this.props.post.date)
                    }
                </p>
                <p className="post-body">
                    {
                        this.props.post.content
                    }
                </p>
                {
                    this.renderComments()
                }
            </Thumbnail>
        );
    }
}
