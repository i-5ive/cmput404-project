import React from "react";
import PropTypes from "prop-types";

/**
 * Displays a singular post
 */
export default class Post extends React.Component {
    static propTypes = {
        className: PropTypes.string.isRequired,
        postId: PropTypes.string.isRequired
    }

    constructor(props) {
        super(props);
        this.getComments = this.getComments.bind(this);
        this.makeComment = this.makeComment.bind(this);
        this.autosize = this.autosize.bind(this);
        this.state = {
            comments: [],
            promiseDone: false
        };
    }

    componentDidMount() {
        this.getComments();

        const textarea = document.getElementById(this.props.postId);

        if (textarea) {
            textarea.addEventListener("keydown", this.autosize);
        }
    }

    autosize() {
        const element = document.getElementById(this.props.postId);
        setTimeout(function() {
            element.style.cssText = `height: ${element.scrollHeight}px`;
        }, 0);
    }

    /**
     * GET's to the database
     */
    getComments() {
        // TODO: actually connect this to the database
        // TODO: currently this will only work locally, perhaps we have to fix that?

        // fetch("http://localhost:8000/api/<POST ID STRING FROM PROPS/comments")
        //   .then(res => res.json())
        //   .then(text => {
        //       this.setState({posts: text});
        //       this.setState({promiseDone: true});
        //   });

        // TODO: remove the 2 lines below. It is fake data so Mandy can make the UI
        this.setState({ comments: ["thing", "thing2"] });
        this.setState({ promiseDone: true });
    }

    /**
     * POST's to the database
     */
    makeComment() {
        // TODO: check if there is anything to post (whote space should not be posted)
        const element = document.getElementById(this.props.postId),
            comment = element.value;
        console.log(comment);
        element.value = "";
        element.style.cssText = "height: 24px";
    }

    render() {
        if (!this.state.promiseDone) {
            console.log("Waiting for DB");
        }
        return (
            <div className={this.props.className}>
                <div className="post-wrapper">
                    <p className="post-title"><strong>
                        I am having an amazing day!</strong>
                    </p>
                    <p className="post-body">
                        I am having a great day because I am working on 404 with my CREW
                    </p>
                </div>
                <div className="comment-wrapper">
                    {this.state.comments.map(comment => (
                        <p className="comment" key={comment}>comment</p>
                    ))}
                    <div className="comment-feild">
                        <textarea className="comment-input" id={this.props.postId} name="text" rows="1" wrap="soft" />
                        <button className="send-comment-button" onClick={this.makeComment}>
                            <i className="fa fa-paper-plane send-comment-button" />
                        </button>
                    </div>
                </div>
            </div>
        );
    }
}

// <input className="comment-input" type="text" id="comment" name="comment"/>
