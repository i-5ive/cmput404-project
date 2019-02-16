import React from "react";

/**
 * This is componenet will allow the user to make a new post
 * This should only be shown if there is a user logged in
 */
export default class NewPostButton extends React.Component {
    //TODO: only allow this to show if there is a user logged in
    // <img src="../../icons/new-post.svg" alt="Make a new post">
    render() {
        return (
            <div>
                <i className="fa fa-pencil-square-o"/>
                <button className="new-post-button" type="button">
                    NewPostButton
                </button>
            </div>
        );
    }
}
